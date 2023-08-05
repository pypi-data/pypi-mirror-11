import bloop.column
import bloop.index
import bloop.util
import declare
MISSING = bloop.util.Sentinel('MISSING')


class __BaseModel(object):
    '''
    DO NOT SUBCLASS DIRECTLY.

    Instead, subclass the `model` attribute of an engine.  This ensures the
    proper metaclass setup has been performed, so that `engine.bind` will
    work.

    Example:

        engine = bloop.Engine()
        BaseModel = engine.model

        class CustomBaseModel(BaseModel):
            # ... cross-model code goes here
    '''
    def __init__(self, **attrs):
        # Only set values from **attrs if there's a
        # corresponding `model_name` for a column in the model
        for column in self.Meta.columns:
            value = attrs.get(column.model_name, MISSING)
            if value is not MISSING:
                setattr(self, column.model_name, value)

    @classmethod
    def __load__(cls, attrs):
        ''' dict -> obj '''
        obj = cls.Meta.bloop_init()
        # Expect all columns on load
        cls.Meta.bloop_engine.__update__(obj, attrs, cls.Meta.columns)
        return obj

    @classmethod
    def __dump__(cls, obj):
        ''' obj -> dict '''
        attrs = {}
        engine = cls.Meta.bloop_engine.type_engine
        for column in cls.Meta.columns:
            value = getattr(obj, column.model_name, MISSING)
            # Missing expected column
            if value is not MISSING:
                attrs[column.dynamo_name] = engine.dump(column.typedef, value)
        return attrs

    def __str__(self):  # pragma: no cover
        def _attr(attr):
            return "{}={}".format(attr, repr(getattr(self, attr, None)))
        attrs = ", ".join(_attr(c.model_name) for c in self.Meta.columns)
        return "{}({})".format(self.__class__.__name__, attrs)
    __repr__ = __str__

    def __hash__(self):  # pragma: no cover
        return super().__hash__()

    def __eq__(self, other):
        ''' Only checks defined columns. '''
        cls = self.__class__
        if not isinstance(other, cls):
            return False
        for column in cls.Meta.columns:
            value = getattr(self, column.dynamo_name, MISSING)
            other_value = getattr(other, column.dynamo_name, MISSING)
            if value != other_value:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


def BaseModel(engine):
    '''
    Although this returns a class, you should NOT call this function to create
    a base model class.  Instead, subclass the `model` attribute of an engine.
    Doing this ensures the proper metaclass setup has been performed,
    so that `engine.bind` will work.

    Example:

        engine = bloop.Engine()
        BaseModel = engine.model

        class CustomBaseModel(BaseModel):
            # ... cross-model code goes here
    '''
    if engine.model:
        raise ValueError("BaseModel already exists for engine")

    class ModelMetaclass(declare.ModelMetaclass):
        def __new__(metaclass, name, bases, attrs):

            model = super().__new__(metaclass, name, bases, attrs)
            Meta = model.Meta
            Meta.write_units = getattr(Meta, "write_units", 1)
            Meta.read_units = getattr(Meta, "read_units", 1)

            # These are sets instead of lists, because set uses __hash__
            # while some list operations uses __eq__ which will break
            # with the ComparisonMixin
            Meta.columns = set(filter(
                lambda f: isinstance(f, bloop.column.Column),
                Meta.fields))
            Meta.indexes = set(filter(
                lambda f: isinstance(f, bloop.index.Index),
                Meta.fields))

            Meta.columns_by_model_name = declare.index(
                Meta.columns, 'model_name')
            Meta.columns_by_dynamo_name = declare.index(
                Meta.columns, 'dynamo_name')

            Meta.hash_key = None
            Meta.range_key = None
            for column in Meta.columns:
                if column.hash_key:
                    if Meta.hash_key:
                        raise ValueError("Model hash_key over-specified")
                    Meta.hash_key = column
                elif column.range_key:
                    if Meta.range_key:
                        raise ValueError("Model range_key over-specified")
                    Meta.range_key = column

            # Look up the current hash key -- which is specified by
            # model_name, not dynamo_name -- in indexed columns and relate
            # the proper `bloop.Column` object
            cols = Meta.columns_by_model_name
            for index in Meta.indexes:
                index.model = model
                if isinstance(index, bloop.index.GlobalSecondaryIndex):
                    index.hash_key = cols[index.hash_key]
                elif isinstance(index, bloop.index.LocalSecondaryIndex):
                    if not Meta.range_key:
                        raise ValueError(
                            "Cannot specify a LocalSecondaryIndex " +
                            "without a table range key")
                    index.hash_key = Meta.hash_key
                else:
                    raise ValueError("Index is an abstract class, must specify"
                                     "LocalSecondaryIndex or"
                                     "GlobalSecondaryIndex")

                if index.range_key:
                    index.range_key = cols[index.range_key]

                projected = index.projection_attributes = set()

                if index.projection == "ALL":
                    projected.update(Meta.columns)
                elif index.projection == "KEYS_ONLY":
                    keys = (Meta.hash_key, Meta.range_key,
                            index.hash_key, index.range_key)
                    projected.update(key for key in keys if key)
                # List of column model_names - convert to `bloop.Column`
                # objects and merge with keys in projection_attributes
                else:
                    keys = (Meta.hash_key, Meta.range_key,
                            index.hash_key, index.range_key)
                    projected.update(key for key in keys if key)
                    attrs = (cols[attr] for attr in index.projection)
                    projected.update(attrs)

                    index.projection = "INCLUDE"

            # Entry point for model population. By default this is the
            # model class. Custom models can specify the Meta
            # attr `bloop_init`, which should be a function taking a
            # **kwarg of name:value pairs corresponding to modeled columns.
            Meta.bloop_init = getattr(Meta, "bloop_init", model)
            Meta.bloop_engine = engine

            Meta.table_name = getattr(Meta, "table_name", model.__name__)

            # If the engine already has a base, register this model.
            # Otherwise, this probably IS the engine's base model
            if engine.model:
                engine.unbound_models.add(model)
            return model
    return ModelMetaclass("Model", (__BaseModel,), {})

# http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ \
#   Expressions.SpecifyingConditions.html#ConditionExpressionReference.Syntax
import operator

missing = object()
EXPRESSION_KEYS = {
    "condition": "ConditionExpression",
    "filter": "FilterExpression",
    "key": "KeyConditionExpression"
}
ATTR_NAMES = "ExpressionAttributeNames"
ATTR_VALUES = "ExpressionAttributeValues"


def render(engine, condition, mode):
    renderer = ConditionRenderer(engine)
    return renderer.render(condition, mode=mode)


class ConditionRenderer:
    def __init__(self, engine):
        self.engine = engine
        self.attr_values = {}
        self.attr_names = {}
        # Reverse index names so we can re-use ExpressionAttributeNames.
        # We don't do the same for ExpressionAttributeValues since they are
        # dicts of {"TYPE": "VALUE"} and would take more space and time to use
        # as keys, as well as less frequently being re-used than names.
        self.name_attr_index = {}
        self.__ref_index = 0

    def value_ref(self, column, value):
        ref = ":v{}".format(self.__ref_index)
        self.__ref_index += 1

        # Dump the value (default to current) through the column's
        # typedef into dynamo's format, then persist a reference
        # in ExpressionAttributeValues
        type_engine = self.engine.type_engine
        dynamo_value = type_engine.dump(column.typedef, value)

        self.attr_values[ref] = dynamo_value

        return ref

    def name_ref(self, column):
        # Small optimization to request size for duplicate name refs
        existing_ref = self.name_attr_index.get(column.dynamo_name, None)
        if existing_ref:
            return existing_ref

        ref = "#n{}".format(self.__ref_index)
        self.__ref_index += 1
        self.attr_names[ref] = column.dynamo_name
        self.name_attr_index[column.dynamo_name] = ref
        return ref

    def render(self, condition, mode):
        rendered_expression = condition.render(self)
        # An expression contains the compressed string, and any name/value ref
        key = EXPRESSION_KEYS[mode]
        expression = {key: rendered_expression}
        if self.attr_names:
            expression[ATTR_NAMES] = self.attr_names
        if self.attr_values:
            expression[ATTR_VALUES] = self.attr_values
        return expression


class BaseCondition:
    def __and__(self, other):
        return And(self, other)
    __iand__ = __and__

    def __or__(self, other):
        return Or(self, other)
    __ior__ = __or__

    def __invert__(self):
        return Not(self)
    __neg__ = __invert__

    def __len__(self):
        return 1


class Condition(BaseCondition):
    '''
    Empty condition that can be used as an initial value for iteratively
    building conditions.

    Usage:
        condition = Condition()
        for foo in bar:
            condition &= Model.field == foo
    '''
    def __and__(self, other):
        return other
    __iand__ = __and__

    def __or__(self, other):
        return other
    __ior__ = __or__

    def __invert__(self):
        return self
    __neg__ = __invert__

    def __len__(self):
        return 0

    def __str__(self):  # pragma: no cover
        return "EmptyCondition()"
    __repr__ = __str__

    def render(self, renderer):
        raise ValueError("Can't render empty condition")


class MultiCondition(BaseCondition):
    def __init__(self, *conditions):
        self.conditions = conditions

    def __str__(self):  # pragma: no cover
        conditions = ", ".join(str(c) for c in self.conditions)
        return self.name + "({})".format(conditions)
    __repr__ = __str__

    def __len__(self):
        return sum(map(len, self.conditions))

    def render(self, renderer):
        if len(self.conditions) == 1:
            return self.conditions[0].render(renderer)
        rendered_conditions = (c.render(renderer) for c in self.conditions)
        conjunction = " {} ".format(self.uname)
        return "(" + conjunction.join(rendered_conditions) + ")"


class And(MultiCondition):
    name = "And"
    uname = "AND"


class Or(MultiCondition):
    name = "Or"
    uname = "OR"


class Not(BaseCondition):
    def __init__(self, condition):
        self.condition = condition

    def __str__(self):  # pragma: no cover
        return "Not({})".format(self.condition)
    __repr__ = __str__

    def __len__(self):
        return len(self.condition)

    def render(self, renderer):
        return "(NOT {})".format(self.condition.render(renderer))


class Comparison(BaseCondition):
    comparator_strings = {
        operator.eq: "=",
        operator.ne: "<>",
        operator.lt: "<",
        operator.gt: ">",
        operator.le: "<=",
        operator.ge: ">=",
    }

    def __init__(self, column, comparator, value):
        if comparator not in self.comparator_strings:
            raise ValueError("Unknown comparator '{}'".format(comparator))
        self.column = column
        self.comparator = comparator
        self.value = value

    def __str__(self):  # pragma: no cover
        return "Compare({}, {}, {})".format(
            self.comparator_strings[self.comparator],
            self.column, self.value)
    __repr__ = __str__

    def render(self, renderer):
        nref = renderer.name_ref(self.column)
        vref = renderer.value_ref(self.column, self.value)
        comparator = self.comparator_strings[self.comparator]
        return "({} {} {})".format(nref, comparator, vref)


class AttributeExists(BaseCondition):
    def __init__(self, column, negate):
        self.column = column
        self.negate = negate

    def __str__(self):  # pragma: no cover
        name = "AttributeNotExists" if self.negate else "AttributeExists"
        return "{}({})".format(name, self.column)
    __repr__ = __str__

    def render(self, renderer):
        name = "attribute_not_exists" if self.negate else "attribute_exists"
        nref = renderer.name_ref(self.column)
        return "({}({}))".format(name, nref)


class BeginsWith(BaseCondition):
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def __str__(self):  # pragma: no cover
        return "BeginsWith({}, {})".format(self.column, self.value)
    __repr__ = __str__

    def render(self, renderer):
        nref = renderer.name_ref(self.column)
        vref = renderer.value_ref(self.column, self.value)
        return "(begins_with({}, {}))".format(nref, vref)


class Contains(BaseCondition):
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def __str__(self):  # pragma: no cover
        return "Contains({}, {})".format(self.column, self.value)
    __repr__ = __str__

    def render(self, renderer):
        nref = renderer.name_ref(self.column)
        vref = renderer.value_ref(self.column, self.value)
        return "(contains({}, {}))".format(nref, vref)


class Between(BaseCondition):
    def __init__(self, column, lower, upper):
        self.column = column
        self.lower = lower
        self.upper = upper

    def __str__(self):  # pragma: no cover
        return "Between({}, {}, {})".format(
            self.column, self.lower, self.upper)
    __repr__ = __str__

    def render(self, renderer):
        nref = renderer.name_ref(self.column)
        vref_lower = renderer.value_ref(self.column, self.lower)
        vref_upper = renderer.value_ref(self.column, self.upper)
        return "({} BETWEEN {} AND {})".format(
            nref, vref_lower, vref_upper)


class In(BaseCondition):
    def __init__(self, column, values):
        self.column = column
        self.values = values

    def __str__(self):  # pragma: no cover
        values = ", ".join(str(c) for c in self.values)
        return "In({}, [{}])".format(self.column, values)
    __repr__ = __str__

    def render(self, renderer):
        nref = renderer.name_ref(self.column)
        values = (renderer.value_ref(self.column, v) for v in self.values)
        values = ", ".join(values)
        return "({} IN ({}))".format(nref, values)

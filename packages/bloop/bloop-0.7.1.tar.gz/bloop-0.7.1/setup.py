""" Setup file """
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.markdown')) as f:
    README = f.read()


def get_version():
    with open('bloop/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

REQUIREMENTS = [
    'arrow',
    'boto3',
    'declare'
]

TEST_REQUIREMENTS = [
    'tox',
    'pytest',
    'coverage',
    'flake8'
]

if __name__ == "__main__":
    setup(
        name='bloop',
        version=get_version(),
        description="ORM for DynamoDB",
        long_description=README,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Software Development :: Libraries'
        ],
        author='Joe Cross',
        author_email='joe.mcross@gmail.com',
        url='https://github.com/numberoverzero/bloop',
        license='MIT',
        keywords='aws dynamo dynamodb orm',
        platforms='any',
        include_package_data=True,
        packages=find_packages(exclude=('tests', 'examples')),
        install_requires=REQUIREMENTS,
        tests_require=REQUIREMENTS + TEST_REQUIREMENTS,
    )

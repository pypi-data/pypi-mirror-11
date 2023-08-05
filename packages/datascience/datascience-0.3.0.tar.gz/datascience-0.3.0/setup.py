import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

install_requires = [
    'numpy',
    'matplotlib',
    'pandas',
    'folium',
    'IPython',
    'jinja2',  # folium dependency
]

tests_requires = [
    'pytest',
    'coverage == 3.7.1',
    'coveralls == 0.5'
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


VERSION = '0.3.0'

setup(
    name = 'datascience',
    packages = ['datascience'],
    version = VERSION,
    install_requires = install_requires + tests_requires,
    tests_require = tests_requires,
    cmdclass = {'test': PyTest},
    description = 'A Jupyter notebook Python library for introductory data science',
    author = 'John DeNero, David Culler, Alvin Wan, Sam Lau',
    author_email = 'ds8-instructors@berkeley.edu',
    url = 'https://github.com/dsten/datascience',
    download_url = 'https://github.com/dsten/datascience/archive/%s.zip' % VERSION,
    keywords = ['data', 'tools', 'berkeley'],
    classifiers = []
)

To use it, pass the module (without .py), or the package name as the autometa keyword argument for
setup()::

    #! /usr/bin/env python
    from setuptools import setup

    setup(
        autometa='test',
        name='Test',
        packages=['test'],
        ...
    )

Setuptools-Autometa will parse the specified module or package's __init__.py and set version to its
__version__ attribute, description to the first line of its docstring, and long_description to the
rest of the docstring. Additionally build_sphinx command's version and release options will be set.

For example following package's __init__.py::

    """First line of docstring.

    Many
    more
    lines
    of
    docstring.
    """
    __version__ = '1.2.3.dev0'  # alternatively: (1, 2, 3, 'dev0')

Is equivalent to writing::

    setup(
        version='1.2.3.dev0',
        description='First line of docstring',
        long_description='Many\nmore\nlines\nof\ndocstring.'
        ...
    )

**NOTE:** Please note, that the version is parsed by running `ast.literal_eval`_ on the right side
of the assignment to __version__, so keep in mind that it can only be a string literal, or a
list/tuple of string/integer literals.

**NOTE:** Setuptools-Autometa assumes a `PEP 0257`_ compliant docstring, that is its first line has
to end with a period and be separated from the description by a blank line.

Additionally you can whitelist which fields are to be parsed by using the autometa_fields keyword
argument and setting it to an iterable of field names ('description', 'long_description', 'version').

.. _`ast.literal_eval`: https://docs.python.org/3/library/ast.html#ast.literal_eval
.. _`PEP 0257`: https://www.python.org/dev/peps/pep-0257


To use it, pass module (without .py), or package name as autometa keyword argument for setup()::

    #! /usr/bin/env python
    from setuptools import setup

    setup(
        autometa='test',
        name='Test',
        packages=['test'],
        ...
    )

Example package __init__.py::

    """First line of docstring.

    Many
    more
    lines
    of
    docstring.
    """
    __version__ = '1.2.3.dev0'  # alternatively: (1, 2, 3, 'dev0')

It will parse specified module file or package's __init__.py and set version to its __version__
attribute, description to first line of its docstring, and long_description to the rest of the
docstring.

**NOTE** Please note, that version is parsed by running
`ast.literal_eval <https://docs.python.org/3/library/ast.html?highlight=ast#ast.literal_eval>`_
on the right side of assignment to __version__, so keep in mind that it can only be a string
literal, or a list/tuple of string/integer literals.

Additionally you can whitelist which fields are to be parsed by using autometa_fields keyword
argument and setting it to an iterable of field names.


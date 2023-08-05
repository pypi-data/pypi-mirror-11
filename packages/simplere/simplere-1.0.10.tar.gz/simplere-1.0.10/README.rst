
| |travisci| |version| |downloads| |supported-versions| |supported-implementations| |wheel|

.. |travisci| image:: https://travis-ci.org/jonathaneunice/simplere.png?branch=master
    :alt: Travis CI build status
    :target: https://travis-ci.org/jonathaneunice/simplere

.. |version| image:: http://img.shields.io/pypi/v/simplere.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/simplere

.. |downloads| image:: http://img.shields.io/pypi/dm/simplere.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/simplere

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/simplere.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/simplere

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/simplere.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/simplere

.. |wheel| image:: https://img.shields.io/pypi/wheel/simplere.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/simplere

A simplified interface to Python's regular expression (``re``)
string search. Eliminates steps and provides
simpler access to results. As a bonus, also provides compatible way to
access Unix glob searches.

Usage
=====

Python regular expressions are powerful, but the language's lack
of an *en passant* (in passing) assignment requires a preparatory
motion and then a test::

    import re

    match = re.search(pattern, some_string)
    if match:
        print match.group(1)

With ``simplere``, you can do it in fewer steps::

    from simplere import *

    if match / re.search(pattern, some_string):
        print match[1]

That's particularly valuable in complex search-and-manipulate
code that requires multiple levels of searching along with
pre-conditions, error checking, and post-match cleanup, formatting,
and actions.

As a bonus,
``simplere`` also provides simple glob access.::

    if 'globtastic' in Glob('glob*'):
        print "Yes! It is!"
    else:
        raise ValueError('OH YES IT IS!')

See `Read the Docs <http://simplere.readthedocs.org/en/latest/>`_
for the full installation and usage documentation.

Notes
=====

 *  See ``CHANGES.rst`` for a historical view of changes.

 *  Automated multi-version testing managed with `pytest
    <http://pypi.python.org/pypi/pytest>`_ and `tox
    <http://pypi.python.org/pypi/tox>`_. Continuous integration testing
    with `Travis-CI <https://travis-ci.org/jonathaneunice/intspan>`_.
    Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

    Successfully packaged for, and
    tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
    3.4, and 3.5 pre-release (3.5.0b3) as well as PyPy 2.6.0 (based on
    2.7.9) and PyPy3 2.4.0 (based on 3.2.5).

 *  The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
    `@jeunice on Twitter <http://twitter.com/jeunice>`_
    welcomes your comments and suggestions.


Installation
============

To install or upgrade to the latest version::

    pip install -U simplere

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade simplere

(You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)

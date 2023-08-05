

| |travisci| |version| |downloads| |supported-versions| |supported-implementations| |wheel|

.. |travisci| image:: https://travis-ci.org/jonathaneunice/simplere.svg?branch=master
    :alt: Travis CI build status
    :target: https://travis-ci.org/jonathaneunice/simplere

.. |version| image:: http://img.shields.io/pypi/v/simplere.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/simplere

.. |downloads| image:: http://img.shields.io/pypi/dm/simplere.svg?style=flat
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

simplere
========

A simplified interface to Python's regular expression (``re``)
string search. Eliminates steps and provides
simpler access to results. As a bonus, also provides compatible way to
access Unix glob searches.

.. toctree::
   :maxdepth: 3

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

Motivation
==========

In the simple examples above, "fewer steps" seems like a small
savings (3 lines to 2). While a 33% savings is a pretty good
optimization, is it really worth using another module and
a quirky *en passant* operator to get it?

In code this simple, maybe not. But real regex-based searching tends
to have multiple, cascading searches, and to be tightly interwoven
with complex pre-conditions, error-checking, and post-match formatting
or actions. It gets complicated fast. When multiple ``re`` matches
must be done, it consumes a lot of "vertical space" and often
threatens to push the number of lines a programmer is viewing at
any given moment beyond the number that can be easily held in working
memory. In that case, it proves valuable to condense what is logically
a single operation ("regular expression test") into a single line
with its conditional ``if``.

This is even more true for the "exploratory" phases of development,
before a program's appropriate structure and best logical boundaries
have been established.  One can always "back out" the condensing *en
passant* operation in later production code, if desired.


Re Objects
==========

``Re`` objects are `memoized <http://en.wikipedia.org/wiki/Memoization>`_
for efficiency, so they compile their pattern just once, regardless of how
many times they're mentioned in a program.

Note that the ``in`` test turns the sense of the matching around (compared
to the standard ``re`` module). It asks "is the given string *in* the set of
items this pattern describes?" To be fancy, the ``Re`` pattern is an
intensionally defined set (namely "all strings matching the pattern"). This
order often makes excellent sense whey you have a clear intent for the test.
For example, "is the given string within the set of *all legitimate
commands*?"

Second, the ``in`` test had the side effect of setting the underscore name
``_`` to the result. Python doesn't support *en passant*
assignment--apparently, no matter how hard you try, or how much
introspection you use. This makes it harder to both test and collect results
in the same motion, even though that's often exactly appropriate. Collecting
them in a class variable is a fallback strategy (see the *En Passant*
section below for a slicker one).

If you prefer the more traditional ``re`` calls::

    if Re(pattern).search(some_string):
        print Re._[1]

``Re`` works even better with named pattern components, which are exposed
as attributes of the returned object::

    person = 'John Smith 48'
    if person in Re(r'(?P<name>[\w\s]*)\s+(?P<age>\d+)'):
        print Re._.name, "is", Re._.age, "years old"
    else:
        print "don't understand '{}'".format(person)

One trick being used here is that the returned object is not a pure
``_sre.SRE_Match`` that Python's ``re`` module returns. Nor is it a subclass.
(That class `appears to be unsubclassable
<http://stackoverflow.com/questions/4835352/subclassing-matchobject-in-python>`_.)
Thus, regular expression matches return a proxy object that
exposes the match object's numeric (positional) and
named groups through indices and attributes. If a named group has the same
name as a match object method or property, it takes precedence. Either
change the name of the match group or access the underlying property thus:
``x._match.property``

It's possible also to loop over the results::

    for found in Re('pattern (\w+)').finditer('pattern is as pattern does'):
        print found[1]

Or collect them all in one fell swoop::

    found = Re('pattern (\w+)').findall('pattern is as pattern does')

Pretty much all of the methods and properties one can access from the standard
``re`` module are available.

Under the Covers
================

``ReMatch`` objects
wrap Python's native``_sre.SRE_Match`` objects (the things that ``re``
method calls return).::

    match = re.match(r'(?P<word>th.s)', 'this is a string')
    match = ReMatch(match)
    if match:
        print match.group(1)    # still works
        print match[1]          # same thing
        print match.word        # same thing, with logical name

But that's a huge amount of boiler plate for a simple test, right? So ``simplere``
*en passant* operator redefining the division operation and proxies the ``re`` result
on the fly to the pre-defined ``match`` object::

    if match / re.search(r'(?P<word>th.s)', 'this is a string'):
        assert match[1] == 'this'
        assert match.word == 'this'
        assert match.group(1) == 'this'

If the ``re`` operation fails, the resulting object is guaranteed to have
a ``False``-like Boolean value, so that it will fall through conditional tests.

Options and Alternatives
========================

If you prefer the look of the less-than (``<``) or less-than-or-equal
(``<=``), as indicators that ``match`` takes the value of the
following function call, they are experimentally supported as aliases
of the division operation (``/``).  You may define your own match
objects, and can use them on memoized ``Re`` objects too. Putting
a few of these optional things together::

    answer = Match()   # need to do this just once

    if answer < Re(r'(?P<word>th..)').search('and that goes there'):
        assert answer.word == 'that'


Bonus: Globs
============

Regular expressions are wonderfully powerful, but sometimes the simpler `Unix glob
<http://en.wikipedia.org/wiki/Glob_(programming)>`_ is works just fine. As a bonus,
``simplere`` also provides simple glob access.::

    if 'globtastic' in Glob('glob*'):
        print "Yes! It is!"
    else:
        raise ValueError('YES IT IS')

If you want to search or test
against multiple patterns at once, ``Glob`` objects take
a variable number of patterns. A match is defined as *any* of the
patterns matching.::

    img_formats = Glob("*.png", "*.jpeg", "*.jpg", "*.gif")
    if filename.lower() in img_formats:
        ... further processing ...

Alternatively, you can splay an existing list into the ``Glob``
constructor with Python's unary star syntax::

    img_formats = "*.png *.jpeg *.jpg *.gif".split()
    if filename.lower() in Glob(*img_formats):
        ... further processing ...


Case-insensitive glob searches are also available::

    bg = InsensitiveGlob('b*')
    if 'bubba' in bg:
        assert 'Bubba' in bg

Globs have their own syntax for case insensitive characters,
but it can be a pain to use. It may be easier to use the
``InsensitiveGlob`` subclass. Or even alias the case-insensitive
version as the main one::

    from simplere import InsensitiveGlob as Glob

.. note:: Case folding / case-insensitive searchs work well in the
    ASCII range, but Unicode characters and case folding is more
    intricate. Basic folding is provided out of the box. It's quite
    adequate for mapping against filename patterns and scuh. Those
    needing more extensive Unicode case folding should consider
    normalizing strings, `as described here
    <http://stackoverflow.com/a/29247821/240490>`_. As the tests
    show, basic Unicode folding works fine everywhere. Using
    Unicode in glob patterns (not just strings to be matched)
    works *only* on Python 3.3 or above.

Notes
=====

 *  Version 1.1 adds multi-pattern and case insensitive Glob subclass.
    Added wheel packaging. Rearranged and extended testing structure.
    Updated setup and docs.

 *  See ``CHANGES.rst`` for a fuller historical view of changes.

 *  Automated multi-version testing managed with `pytest
    <http://pypi.python.org/pypi/pytest>`_ and `tox
    <http://pypi.python.org/pypi/tox>`_. Continuous integration testing
    with `Travis-CI <https://travis-ci.org/jonathaneunice/intspan>`_.
    Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

    Successfully packaged for, and
    tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
    3.4, and 3.5 pre-release (3.5.0b3) as well as PyPy 2.6.0 (based on
    2.7.9) and PyPy3 2.4.0 (based on 3.2.5).

 *  ``simplere`` is one part of a larger effort to explore extensions to
    current Python idioms. Its partners include `intensional
    <http://pypi.python.org/pypi/intensional>`_ (intensional sets, which
    also contains a parallel implementation of ``Re``), `enpassant
    <http://pypi.python.org/pypi/enpassant>`_ (more general *en passant*
    assignment), and `withref <https://pypi.python.org/pypi/withref>`_ (an
    alternate take on multi-level object dereferencing).

 *  The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
    `@jeunice on Twitter <http://twitter.com/jeunice>`_
    welcomes your comments and suggestions.

Installation
============

To install or upgrade to the latest version::

    pip install -U simplere

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade simplere

(You may need to prefix these with ``sudo`` to authorize installation. In
environments without super-user privileges, you may want to use ``pip``'s
``--user`` option, to install only for a single user, rather than
system-wide.)
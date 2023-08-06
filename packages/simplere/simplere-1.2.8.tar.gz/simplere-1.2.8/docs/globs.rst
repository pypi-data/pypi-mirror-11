Globs
=====

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

.. note:: Case folding / case-insensitive searches work well in the
    ASCII range, but Unicode characters and case folding is more
    intricate. Basic folding is provided out of the box. It's quite
    adequate for mapping against common
    filename patterns, for example. Those
    needing more extensive Unicode case folding should consider
    normalizing strings, `as described here
    <http://stackoverflow.com/a/29247821/240490>`_. As the tests
    show, basic Unicode folding works fine everywhere. Using
    Unicode in glob patterns (not just strings to be matched)
    works *only* on Python 3.3 or above.


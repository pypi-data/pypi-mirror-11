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

In addition to its own classes, ``from simplere import *`` imports both
the standard ``re`` module and the ``match`` object so you don't have to.


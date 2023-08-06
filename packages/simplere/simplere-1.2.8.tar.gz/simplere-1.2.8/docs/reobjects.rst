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


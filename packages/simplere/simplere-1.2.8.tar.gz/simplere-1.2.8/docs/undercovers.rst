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


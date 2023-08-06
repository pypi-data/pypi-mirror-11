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



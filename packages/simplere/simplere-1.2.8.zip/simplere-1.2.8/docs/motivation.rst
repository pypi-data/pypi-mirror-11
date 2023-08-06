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



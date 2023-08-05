
| |version| |downloads| |supported-versions| |supported-implementations|

.. |version| image:: http://img.shields.io/pypi/v/intspan.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/intspan

.. |downloads| image:: http://img.shields.io/pypi/dm/intspan.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/intspan

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/intspan.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/intspan

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/intspan.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/intspan


Subset of ``set`` designed to conveniently hold sets of integers. It creates
them from, and displays them as, integer spans (e.g. ``1-3,14,29,92-97``).
When iterating, ``pop()``-ing an item, or converting to a list, ``intspan``
behaves as if it were an ordered collection.

The main draw is that this provides a convenient way to specify ranges--for
example, ranges of rows to be processed in a spreadsheet. It can also help
you quickly identify which items were *not* successfully processed in a
large dataset.

Usage
=====

::

    from intspan import intspan

    s = intspan('1-3,14,29,92-97')
    s.discard('2,13,92')
    print s
    print repr(s)
    print list(s)

yields::

    1,3,14,29,93-97
    intspan('1,3,14,29,93-97')
    [1, 3, 14, 29, 93, 94, 95, 96, 97]

While::

    for n in intspan('1-3,5'):
        print n                 # Python 2

yields::

    1
    2
    3
    5

Most set operations such as intersection, union, and so on are available just
as they are in Python's ``set``. In addition, if you wish to extract the
contiguous ranges::

    for r in intspan('1-3,5,7-9,10,21-22,23,24').ranges():
        print r                 # Python 2

yields::

    (1, 3)
    (5, 5)
    (7, 10)
    (21, 24)

Note that these are the endpoints of
`closed intervals <http://en.wikipedia.org/wiki/Interval_(mathematics)>`_,
rather than the half-open intervals Python's ``range()`` function expects.
If you want to use these with Python generators, you'll have to increment
the stop value yourself.

There is a corresponding constructor::

    print intspan.from_ranges([ (4,6), (10,12) ])

Gives::

    4-6,10-12

There is a convenience method ``from_range`` that will create a contiguous
``intspan`` from a given low value to a high value.

To find the elements *not* included in the set::

    items = intspan('1-3,5,7-9,10,21-24')
    print items.complement()

Displays a list of the "missing" elements::

    4,6,11-20

This is computed as any integers between the ``intspan``'s minimum and
maximum values that aren't included. If you'd like to customize the intended
``low`` and ``high`` bounds, you can give those explicitly.::

    print items.complement(high=30)

Yields::

    4,6,11-20,25-30

You can use the ``difference`` method or ``-`` operator if you want
to find the complement with respect to an arbitrary set.

Experimental
============

As of version 1.2, an experimental function ``spanlist`` is provided. It
returns a list from the same kind of specification string as ``intspan``,
but ordered. A corresponding class ``intspanlist`` subclasses ``list`` in
the same way that ``intspan`` subclasses ``set``. But whereas ``intspan``
attempts to faithfully implement the attributes of a Python ``set``,
``intspanlist`` is a thin, experimental shim. In particular, it does not
(yet) seek to allow the same range of modifications a full ``list`` does.
While ``append`` and ``extend`` operations work to maintain a
"set-ish," no-repeats nature, ``insert`` and other ``list`` update
methods provide no such promises. Also, unlike with the core
``intspan`` objects, tests are not (yet) nearly exhaustive.::

    isl = intspanlist('4,1-5,5')
    print repr(isl)
    print list(isl)
    print spanlist('4,1-5,5')

Yields::

    intspanlist('4,1-3,5')
    [4, 1, 2, 3, 5]
    [4, 1, 2, 3, 5]

The intended use case for this ordered version of ``intspan`` is
to help users and developers specify the ordering of elements. For example,
a program might have 20 items, 1-20. If you wanted to process item 7,
then item 3, then "all the rest," ``intspanlist('7,3,1-20')``
would be a convenient way to specify this ordering. You could loop over
that object in the desired order.

Note that ``intspanlist`` objects do not necessarily display as they are
entered, but as an equivalent (lower-level) representation that more
explicitly maps to the gaps in their ranges. For example::

    >>> intspanlist('7,3,1-20')
    intspanlist('7,3,1-2,4-6,8-20')

Which is equivalent, but more verbose.

Final warning: ``intspanlist`` objects are newly introduced, experimental at this
point, and more loosely tested than the rest of this module.

Performance
===========

``intspan`` piggybacks Python's ``set``, so it stores every integer
individually. Unlike Perl's ``Set::IntSpan`` it is not optimized for long
contiguous runs. For sets of several hundred or even many thousands of
members, you will probably never notice the difference.

On the other hand, if you're doing lots of processing of large sets (e.g.
with 100,000, 1M, or more elements), or doing lots of set operations on them
(e.g. union, intersection), a data structure based on
lists of ranges, `run length encoding
<http://en.wikipedia.org/wiki/Run-length_encoding>`_, or `Judy arrays
<http://en.wikipedia.org/wiki/Judy_array>`_ might perform / scale
better.

Alternatives
============

There are several modules you might want to consider as alternatives or
supplements. AFAIK, none of them provide the convenient integer span
specification that ``intspan`` does, but they have other virtues:

 *  `cowboy <http://pypi.python.org/pypi/cowboy>`_ provides
    generalized ranges and multi-ranges. Bonus points for the package
    tagline: "It works on ranges."

 *  `ranger <http://pypi.python.org/pypi/ranger>`_ is a generalized range and range set
    module. It supports open and closed ranges, and includes mapping objects that
    attach one or more objects to range sets.

 *  `rangeset <http://pypi.python.org/pypi/rangeset>`_ is a generalized range set
    module. It also supports infinite ranges.

 *  `judy <http://pypi.python.org/pypi/judy>`_ a Python wrapper around Judy arrays
    that are implemented in C. No docs or tests to speak of.

Notes
=====

 *  Version 1.2.0 adds an experimental ``spanlist`` constructor.

 *  Version 1.1.0 adds ``from_range`` and ``complement`` methods; improves
    error handling of ``pop`` on an empty set), and tweaks testing.

 *  Patch versions through 1.0.3 are minor bumps, with small testing and
    documentation improvements.

 *  Version 1.0 immediately follows 0.73. Bumped to institute a
    cleaner "semantic versioning" scheme. Upgraded from "beta" to
    "production" status.

 *  Version 0.73 updates testing to include the latest Python 3.4

 *  Version 0.7 fixed parsing of spans including negative numbers, and
    added the ``ranges()`` method. As of 0.71, the ``from_ranges()``
    constructor appeared.

 *  Though inspired by Perl's `Set::IntSpan <http://search.cpan.org/~swmcd/Set-IntSpan/IntSpan.pm>`_,
    that's where the similarity stops.
    ``intspan`` supports only finite sets, and it
    follows the methods and conventions of Python's ``set``.

 *  ``intspan`` methods and operations such as ``add()`` ``discard()``, and
    ``>=`` take integer span strings, lists, and sets as arguments, changing
    facilities that used to take only one item into ones that take multiples,
    including arguments that are technically string specifications rather than
    proper ``intspan`` objects.

 *  String representation and ``ranges()`` method
    based on Jeff Mercado's concise answer to `this
    StackOverflow question <http://codereview.stackexchange.com/questions/5196/grouping-consecutive-numbers-into-ranges-in-python-3-2>`_.
    Thank you, Jeff!

 *  Automated multi-version testing managed with the wonderful
    `pytest <http://pypi.python.org/pypi/pytest>`_,
    `pytest-cov <http://pypi.python.org/pypi/pytest>`_,
    and `tox <http://pypi.python.org/pypi/tox>`_.
    Successfully packaged for, and tested against, all late-model versions of
    Python: 2.6, 2.7, 3.2, 3.3, and 3.4, as well as PyPy 2.6.0 (based on 2.7.9)
    and PyPy3 2.4.0 (based on 3.2.5). Should run fine on Python 3.5, though
    py.test broken on its pre-release iterations.
    Test line coverage ~100%.

 *  The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
    `@jeunice on Twitter <http://twitter.com/jeunice>`_
    welcomes your comments and suggestions.

Installation
============

To install the latest version::

    pip install -U intspan

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade intspan

(You may need to prefix these with "sudo " to authorize installation. In
environments without super-user privileges, you may want to use ``pip``'s
``--user`` option, to install only for a single user, rather than
system-wide.)

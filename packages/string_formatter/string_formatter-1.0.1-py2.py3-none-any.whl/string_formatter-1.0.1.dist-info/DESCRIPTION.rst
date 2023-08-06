================
string_formatter
================

This package is a backport of ``string.Formatter`` and its tests
to Python 2.7 and 3.3 (and 3.4.0 as shipping with Ubuntu 14.04
LTS/Linux Mint 17)

It allows empty keys in format strings as introduced in Python 3.4.1, and
fixes a bug ( ``"{:<{}} {}"`` ) when using nested empty keys, that is
available in all versions of ``string.Formatter()`` allowing empty keys (up
to at least 3.5.0rc3).

Usage
-----

The package can be used as a replacement for ``string``::

    import string_formatter as string

TrailingFormatter
-----------------

Additionally this package includes ``TrailingFormatter`` allow a type
specification `t` with a single character parameter, that will be added to
the (stringified) value before applying (left-aligned) formatting::


    import string_formatter as string

    fmt = string.TrailingFormatter()
    d = dict(a=1, bc=2, xyz=18)
    for key in sorted(d):
        print(fmt.format("{:t{}<{}} {:>3}", key, ':', 15, d[key]))

giving::

    a:                1
    bc:               2
    xyz:             18





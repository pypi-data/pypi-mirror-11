
| |travisci| |version| |downloads| |supported-versions| |supported-implementations| |wheel|

.. |travisci| image:: https://api.travis-ci.org/jonathaneunice/namedentities.svg
    :target: http://travis-ci.org/jonathaneunice/namedentities

.. |version| image:: http://img.shields.io/pypi/v/namedentities.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/namedentities

.. |downloads| image:: http://img.shields.io/pypi/dm/namedentities.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/namedentities

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/namedentities.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/namedentities

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/namedentities.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/namedentities

.. |wheel| image:: https://img.shields.io/pypi/wheel/namedentities.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/namedentities

.. |oplus| unicode:: 0x2295 .. oplus

When reading HTML, named entities are neater and often easier to comprehend
than numeric entities (in decimal or hexidecimal notation), Unicode
characters, or a mixture. The |oplus| character, for example, is easier to
recognize and remember as ``&oplus;`` than ``&#8853;`` or ``&#x2295;`` or
``\u2295``.

Because they use only pure ASCII characters, entities are also much safer to
use in databases, files, emails, and other contexts, especially given the
many endings (UTF-8 and such) required to fit Unicode into byte-oriented
storage, and the many quirks and platform variations seen along the way.

This module helps convert from whatever mixture of characters and/or
entities you have into named HTML entities. Or, if you prefer, it will help
you render them into numeric HTML entities (using either the decimal or
hexadecimal numbering scheme). Finally, it will help you go the other way,
mapping all entities into Unicode.

Usage
=====

Python 2::

    from namedentities import *

    u = u'both em\u2014and&#x2013;dashes&hellip;'

    print "named:  ", repr(named_entities(u))
    print "numeric:", repr(numeric_entities(u))
    print "hex:"   ", repr(hex_entities(u))
    print "unicode:", repr(unicode_entities(u))

yields::

    named:   'both em&mdash;and&ndash;dashes&hellip;'
    numeric: 'both em&#8212;and&#8211;dashes&#8230;'
    hex:     'both em&#x2014;and&#x2013;dashes&#x2026;'
    unicode: u'both em\u2014and\u2013dashes\u2026'

You can do just about the same thing in Python 3, but you have to use a
``print`` function rather than a ``print`` statement, and prior to 3.3, you
have to skip the ``u`` prefix that in Python 2 marks string literals as
being Unicode literals. In Python 3.3 and following, however, you can start
using the ``u`` marker again, if you like. While all Python 3 strings are
Unicode, it helps with cross-version code compatibility. (You can use the
``six`` cross-version compatibility library, as the tests do.)

One good use for ``unicode_entities`` is to create cross-platform,
cross-Python-version strings that conceptually contain
Unicode characters, but spelled out as named (or numeric) HTML entities. For
example::

    unicode_entities('This &rsquo;thing&rdquo; is great!')

This has the advantage of using only ASCII characters and common
string encoding mechanisms, yet rendering full Unicode strings upon
reconstitution.  You can use the other functions, say ``named_entities()``,
to go from Unicode characters to named entities.

Other APIs
==========

``entities(text, kind)`` takes text and the kind of entities
you'd like returned. ``kind`` can be ``'named'`` (the default), ``'numeric'``,
``'hex'``, ``'unicode'``, or ``'none'``. It's an alternative to the
more explicit individual functions such as ``named_entities``.

``unescape(text)`` changes all entities into Unicode characters. It has an
alias, ``unicode_entities(text)`` for parallelism with the other APIs.

Encodings Akimbo
================

This module helps map string between HTML entities (named, numeric, or hex)
and Unicode characters. It makes those mappings--previously somewhat obscure
and nitsy--easy. Yay us! It will not, however, specifically help you with
"encodings" of Unicode characters such as UTF-8; for these, use Python's
built-in features.

Python 3 tends to handle encoding/decoding pretty transparently.
Python 2, however, does not. Use the ``decode``
string method to get (byte) strings including UTF-8 into Unicode;
use ``encode`` to convert true ``unicode`` strings into UTF-8. Please convert
them to Unicode *before* processing with ``namedentities``::

    s = "String with some UTF-8 characters..."
    print named_entities(s.decode("utf-8"))

The best strategy is to convert data to full Unicode as soon as
possible after ingesting it. Process everything uniformly in Unicode.
Then encode back to UTF-8 etc. as you write the data out. This strategy is
baked-in to Python 3, but must be manually accomplished in Python 2.

Notes
=====

 * See ``CHANGES.rst`` for historical changes.

 * Doesn't attempt to encode ``&lt;``, ``&gt;``, or
   ``&amp;`` (or their numerical equivalents) to avoid interfering
   with HTML escaping.

 * Automated multi-version testing managed with `pytest
   <http://pypi.python.org/pypi/pytest>`_  and `tox
   <http://pypi.python.org/pypi/tox>`_. Continuous integration testing
   with `Travis-CI <https://travis-ci.org/jonathaneunice/namedentities>`_.
   Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

   Successfully packaged for, and
   tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
   3.4, and 3.5 pre-release (3.5.0b3) as well as PyPy 2.6.0 (based on
   2.7.9) and PyPy3 2.4.0 (based on 3.2.5).

 * This module started as basically a packaging of `Ian Beck's recipe
   <http://beckism.com/2009/03/named_entities_python/>`_. While it's
   moved forward since then, Ian's contribution to the core remains
   key. Thank you, Ian!

 * The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_
   or `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes
   your comments and suggestions.


Installation
============

To install or upgrade to the latest version::

    pip install -U namedentities

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade namedentities

(You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)

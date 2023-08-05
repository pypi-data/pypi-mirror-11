
| |version| |downloads| |supported-versions| |supported-implementations|

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

.. |oplus| unicode:: 0x2295 .. oplus

When reading HTML, named entities are often neater and easier to comprehend
than numeric entities, Unicode (or other charset) characters, or a mixture
of all of the above. The |oplus| character, for example, is easier to
recognize and remember as ``&oplus;`` than ``&#8853;`` or ``&#x2295;``
or ``\u2295``.

Because they fall within the ASCII range, entities are
also much safer to use in multiple contexts than Unicode and its various
encodings (UTF-8 and such).

This module helps convert from whatever characters or entities you have into
named HTML entities. If you prefer entities of the counting type, it will
render those (either decimal or hexadecimal). Or, if you prefer, it will
help you go the other way, mapping all entities into Unicode. B

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
``print`` function rather than a ``print`` statement, and prior to 3.3, you have
to skip the ``u`` prefix that in Python 2 marks string literals as being Unicode
literals. In Python 3.3 and following, however, you can start using the ``u``
marker again, if you like. While all Python 3 strings are Unicode, it helps
with cross-version code compatibility. (You can use the ``six`` cross-version
compatibility library, as the tests do.)

One good use for ``unicode_entities`` is to create cross-platform,
cross-Python-version strings that conceptually contain
Unicode characters, but spelled out as named (or numeric) HTML entities. For
example::

    unicode_entities('This &rsquo;thing&rdquo; is great!')

This has the advantage of using only ASCII characters and common
string encoding mechanisms, yet rendering full Unicode strings upon
reconstitution.  You can use the other functions, say ``named_entities()``,
to go from Unicode characters to named entities.

Alternate API
=============

A new function ``entities(text, kind)`` takes text and the kind of entities
you'd like returned. ``kind`` can be ``'named'`` (the default), ``'numeric'``,
``'hex'``, ``'unicode'``, or ``'none'``.

Encodings Akimbo
================

This module will help you map between HTML entities and Unicode characters,
whichever style you prefer. It will not, however, specifically help you with
"encodings" of Unicode characters such as UTF-8; for these, use the built-in
``decode`` string method (to get Unicode from UTF-8) and ``encode`` (to
convert Unicode into UTF-8).

This is more an issue in Python 2, which makes Unicode a manual process. If
you have (byte) strings containing UTF-8 (or other encoded) characters,
please convert them to Unicode before processing with ``namedentities``::

    s = "String with some UTF-8 characters..."
    print named_entities(s.decode("utf-8"))

Good advice for Python 2 is to convert data to full Unicode as soon as
possible after reading it or otherwise ingesting it. Process in Unicode.
Then encode back to UTF-8 etc. when you write the data out. This strategy is
baked-in to Python 3, so needs to be less explicitly managed there.

Recent Changes
==============

 * 1.6.5 updates the testing matrix, packaging, and documentation.
   All vestiges of support for Python 2.5 and PyPy 1.9 and earlier
   are officially withdrawn; if you're still back there, upgrade alredy!

 * As of 1.6.4, ``decimal_entities()`` is a synonym for ``numeric_entities()``.

 * As of 1.6.3, ``entities()`` raises a bespoke ``UnknownEntities`` class rather
   that ``KeyError`` if you request an unknown type of entities. More important,
   an old version of ``namedentities`` that was interfering with automated ``pip``
   installations has been removed from PyPI.

 * As of 1.6, ``entities()`` API added. A slightly different import mechanism is used.

 * The ``numeric_entities(text)`` and ``hex_entities(text)`` APIs have been
   added, shifting the module's mission from "named entities" to "general
   purpose entity transformation." Live and learn!

 * The ``unescape(text)`` API changes all entities into Unicode characters.
   While long present, is now available for easy external consumption. It has an
   alias, ``unicode_entities(text)`` for parallelism with the other APIs.

 * Repackaged first as a Python package, rather than independent modules. Then,
   given my growing confidence in managing cross-version packages, previously
   separate backend implementations for Python 2 and Python 3 have been merged
   into a single backend.

 * Automated multi-version testing managed with the wonderful `pytest
   <http://pypi.python.org/pypi/pytest>`_ and `tox
   <http://pypi.python.org/pypi/tox>`_. Successfully packaged for, and
   tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
   and 3.4, as well as PyPy 2.6.0 (based on 2.7.9) and PyPy3 2.4.0 (based
   on 3.2.5). Should run fine on Python 3.5, though py.test is broken on
   its pre-release iterations.

Notes
=====

 * Doesn't attempt to encode ``&lt;``, ``&gt;``, or
   ``&amp;`` (or their numerical equivalents) to avoid interfering
   with HTML escaping.

 * This module started as basically a packaging of `Ian Beck's recipe
   <http://beckism.com/2009/03/named_entities_python/>`_. While it's
   moved forward since then, it's still mostly Ian under the
   covers. Thank you, Ian!

Installation
============

To install or upgrade to the latest version::

    pip install -U namedentities

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade namedentities

(You may need to prefix these with ``sudo`` command to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)



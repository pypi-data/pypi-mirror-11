
Change Log
==========

 * 1.6.8 adds wheel packaging and updates testing config.

 * 1.6.7 switches from BSD to Apache License 2.0 and integrates
   ``tox`` testing with ``setup.py``

 * 1.6.6 improves docs. Adds testing under Travis CI.

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

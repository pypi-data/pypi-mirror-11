Changelog
=========

0.1.6 (2015-08-03)
------------------

Added:

- `waffle.io`_ page to documentation for project management overview

Fixed:

- Parse errors when RAML file would have empty mappings (`Issue 30`_)
- Switch ``yaml.Loader`` to ``yaml.SafeLoader`` (`Issue 26`_)
- Update documentation to reflect rearrangement of errors (`Issue 27`_)
- Remove ``default`` parameter from being required for ``baseURIParameters`` (`Issue 29`_)
- Pin mock library for tox tests (`Issue 22`_)
- Experimenting with speeding up pypy tests within tox on Travis

0.1.5 (2015-06-05)
------------------

Fixed:

- Configuration parsing for validation/production.  Thanks `vrajmohan`_!
- Parsing of response bodies (fixes `Issue 12`_).  Thanks `Igor`_!

0.1.4 (2015-05-27)
------------------

Added:

- Support for recursive ``!includes`` in RAML files (0.1.3 would handle the error, now actually supports it. Thanks `Ben`_ for your `PR`_!).

0.1.3 (2015-05-14)
------------------

Added:

- New ``#ramlfications`` channel on `freenode`_ (web chat link)! Come chat, I'm lonely.
- Documentation for configuration and the ``update`` command.

Fixed:

- Handle recursive/cyclical ``!includes`` in RAML files for now (`PR`_)
- Encoding issues from upgrading to tox 2.0
- ``tests/test_utils.py`` would create ``ramlfications/data/supported_mime_types.json``; now mocked out.

0.1.2 (2015-04-21)
------------------

Fixed:

- pypy 2.5.x would fail a parser test because order of list was not expected

0.1.1 (2015-04-21)
------------------

New:

- Added ability to parse IANA-supported MIME media types
- Added ``update`` command for user to update IANA-supported MIME types if/when needed

0.1.0a1 (2015-04-18)
--------------------
Initial alpha release of ``ramlfications``\!


.. _`PR`: https://github.com/spotify/ramlfications/pull/8
.. _`freenode`: http://webchat.freenode.net?channels=%23ramlfications&uio=ND10cnVlJjk9dHJ1ZQb4
.. _`Ben`: https://github.com/benhamill
.. _`vrajmohan`: https://github.com/spotify/ramlfications/pull/16
.. _`Issue 12`: https://github.com/spotify/ramlfications/issues/12
.. _`Igor`: https://github.com/spotify/ramlfications/pull/13
.. _`Issue 30`: https://github.com/spotify/ramlfications/issues/30
.. _`Issue 26`: https://github.com/spotify/ramlfications/issues/26
.. _`Issue 27`: https://github.com/spotify/ramlfications/issues/27
.. _`Issue 29`: https://github.com/spotify/ramlfications/issues/29
.. _`Issue 22`: https://github.com/spotify/ramlfications/issues/22
.. _`waffle.io`: https://waffle.io/spotify/ramlfications

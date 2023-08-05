Change Log
==========

1.1.3 (August 3, 2015)
''''''''''''''''''''''

  * Cloning and changing of ``Quoter`` instances (though not yet
    ``HTMLQuoter`` or ``XMLQuoter`` instances) is now operational.

1.1.0 (August 3, 2015)
''''''''''''''''''''''

  * Cleaned up HTML quoting, esp. re void / self-closing elements.
    Added new double-backtick functions. Changed to Apache License 2.0.
    Updated docs and testing matrix.

1.0.3 (November 1, 2013)
''''''''''''''''''''''''

  * HTML, XML, and lambda quoters now use class-relative styles dictionaries,
    as opposed to piggybacking the standard Quoter styles dictionary.
  * Improved docs and tests.
  * Added ``lambdaq`` front-end parallel to ``quote``, ``html``, and ``xml``.

1.0.2 (October 31, 2013)
''''''''''''''''''''''''

  * Some internal cleanups to improve code reuse among classes. Bumped
    from Alpha to Beta status.

1.0.1 (October 31, 2013)
''''''''''''''''''''''''

  * A new alternate API consisting of attribute names off of a default
    quoting object (e.g. ``quote.single`` as a specialization of ``quote``)
    has been instituted. This is mostly, but not perfectly, a superset of the
    previous use of a ``quote()`` function.
  * The naming infrastructure has been beefed up, with multiple names (aliases)
    possible for all named objects.
  * A new ``XMLQuoter`` is inserted as a superclass of ``HTMLQuoter`. It has
    ``HTMLQuoter``'s ability to parse CSS style id and class name definitions
    (e.g. ``'#first.big.special'``), as well as namespace support (new ``ns``
    attribute).
  * XML and HTML quoters for individual tags are automagically generated upon
    first use. E.g. ``html.b('this')`` creates an ``HTMLQuoter(tag='b', name='b')``
    quoter that is cached as ``html.b`` for subsequent uses.
  * Updated versioning strategy to comply with `PEP 386 <http://www.python.org/dev/peps/pep-0386/>`_
  * Various other structural and packaging cleanups. E.g. moved into proper
    Python package; given introspectable version number; removed old ``verno``
    auto-update of version number; this proper change long instituted; etc.

0.308 (October 30, 2012)
''''''''''''''''''''''''

  * Last version before PEP 386 versioning switch. Upgrade away from
    these old versions if for no other reason than improving the
    auto-install logic.

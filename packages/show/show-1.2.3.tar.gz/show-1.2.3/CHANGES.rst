Change Log
----------

1.2.3 (August 25, 2015)
'''''''''''''''''''''''

* Code cleanups and additional testing. Test coverage now 77%.

1.2.1 (August 21, 2015)
'''''''''''''''''''''''

* Added ability to give ``@show.inout`` decorator its own parameters.
  Deprecated ``@show.retval``, which is now redunant with
  ``@show.inout(only='out')``.

* Test coverage bumped to 71%.


1.2.0 (August 18, 2015)
'''''''''''''''''''''''

* Added ``show.where()`` as a marker for "where am I now?"
  Improved docs, esp. for ``where``, ``inout``, and ``retval``
  methods. Improved testing. Now at 67% line coverage.

1.1.1 (August 17, 2015)
'''''''''''''''''''''''

* Updated testing strategy to integrate automated test coverage metrics.
  Immediate test and code improvements as a result. Initial coverage was
  53%. Releasing now at 57%.

* Clearly backed out Python 3.5 support for the moment.
  The AST ``Call`` signature has changed notably. Will need
  to deep-dive to fix that.

1.1.0 (August 16, 2015)
'''''''''''''''''''''''

  * Fixed problem with underlying ``say`` object interactions.
    Some doc and testing tweaks.

1.0.4 (July 22, 2015)
'''''''''''''''''''''

  * Updated config, docs, and testing matrix.

1.0.2 (September 16, 2013)
''''''''''''''''''''''''''

  * Improved pretty printing of code snippets for ``@show.inout``
    and ``@show.retval`` decorators.
  * Made ``show`` also accept lambdas to link to variable values.
  * Added ``noshow`` object for easy turning off of showing.
  * General cleanups. Tightened imports. Tweaked docs. Switched to
    ``FmtException`` from ``say>=1.0.4``, and separated extensions
    into own module.
  * Drove version information into ``version.py``

1.0.1 (September 2013)
''''''''''''''''''''''

  * Moved main documentation to Sphinx format in ./docs, and hosted
    the long-form documentation on readthedocs.org. README.rst now
    an abridged version/teaser for the module.

1.0 (September 2013)
''''''''''''''''''''

  * Improved robustness for interactive use. If names cannot be
    detected, still gives value result with ``?`` pseudo-name.
  * Improved type names for ``show.dir`` and ``show.props``
  * Improved ``show.inout`` with full call string on function
    return. A bit verbose in small tests, but too easy to lose
    "what was this called with??" context in real-scale usage
    unless there is clear indication of how the function was
    called.
  * Improved omission of probably useless display properties
    via ``omit`` keyword.
  * Began to add support for showing properties even when proxied through
    another object. Currently limited to selected SQLAlchemy and
    Flask proxies. More
    to come.
  * Cleaned up source for better (though still quite imperfect),
    PEP8 conformance
  * Bumped version number to 1.0 as part of move to `semantic
    versioning <http://semver.org>`_, or at least enough of it so
    as to not screw up Python installation procedures (which don't
    seem to understand 0.401 is a lesser version that 0.5, because
    401 > 5).
  * Probably several other things I've now forgotten.

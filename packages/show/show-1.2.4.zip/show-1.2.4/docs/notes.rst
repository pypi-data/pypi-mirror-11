Notes
=====

* ``show`` is in its early days. Over time, it will provide additional
  context-specific output helpers. For example, the "diff" views of ``py.test``
  seem a high-value enhancement.

* ``show`` depends on introspection, with its various complexities and
  limitations. It assumes that all objects are new-style classes, and that
  your program has not excessively fiddled with class data. Diverge from these
  assumptions, and all bets are off.

* Automated multi-version testing managed with the wonderful `pytest
  <http://pypi.python.org/pypi/pytest>`_ and `tox
  <http://pypi.python.org/pypi/tox>`_. Successfully packaged for, and
  tested against, most late-model versions of Python: 2.7, 3.2, 3.3,
  and 3.4, as well as PyPy 2.6.0 (based on 2.7.9) and PyPy3 2.4.0 (based on
  3.2.5). Currently experiencing issues with Python 2.6 and 3.5, though
  neither of those is currently a mainstream release.

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
  `@jeunice on Twitter <http://twitter.com/jeunice>`_
  welcomes your comments and suggestions.

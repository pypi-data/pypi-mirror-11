| |version| |downloads| |supported-versions| |supported-implementations| |wheel| |coverage|

.. |version| image:: http://img.shields.io/pypi/v/show.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/show

.. |downloads| image:: http://img.shields.io/pypi/dm/show.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/show

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/show.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/show

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/show.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/show

.. |wheel| image:: https://img.shields.io/pypi/wheel/show.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/show

.. |coverage| image:: https://img.shields.io/badge/test_coverage-57%25-87CEFA.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/show

::

    from show import *

    x = 12
    nums = list(range(4))

    show(x, nums)

yields::

    x: 12  nums: [0, 1, 2, 3]

Output is self-labeled, so you don't spend time
doing that yourself.

Debug Printing
==============

Logging, assertions, unit tests, and interactive debuggers are all great
tools. But sometimes you just need to print values as a program runs to see
what's going on. Every language has features to print text, but they're
rarely customized for printing debugging information. ``show`` is. It
provides a simple, DRY mechanism to "show what's going on."

Sometimes programs print so that users can see things, and sometimes they
print so that develpopers can. ``show()`` is for developers, helping rapidly
print the current state of variables in ways that easily indentify what
value is being printed, without a lot of wasted effort. It replaces the
craptastic repetitiveness of::

    print "x: {0}".format(x)

with::

    show(x)

If you'd like to see where the data is being produced,::

    show.set(where=True)

will turn on location reporting. This can also be set on call-by-call basis.

You can also easily distinguish your debugging information from all of the normal
program output. For example::

    show.say.set(style='green')

Will print all of your debugging information in, you guessed it, green.

For this and much more, see `the full documentation at Read the Docs
<http://show.readthedocs.org/en/latest/>`_.

.. note:: There are known issues about running this on Python 2.6 and 3.5,
    and on Windows.


| |version| |downloads| |versions| |impls| |wheel| |coverage|

.. |version| image:: http://img.shields.io/pypi/v/show.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/show

.. |downloads| image:: http://img.shields.io/pypi/dm/show.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/show

.. |versions| image:: https://img.shields.io/pypi/pyversions/show.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/show

.. |impls| image:: https://img.shields.io/pypi/implementation/show.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/show

.. |wheel| image:: https://img.shields.io/pypi/wheel/show.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/show

.. |coverage| image:: https://img.shields.io/badge/test_coverage-67%25-00BFFF.svg
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
print so that developers can. ``show()`` is for developers, helping rapidly
print the current state of variables in ways that easily identify what
value is being printed, without a lot of wasted effort. It replaces the
craptastic repetitiveness of::

    print "x: {0!r}".format(x)

with::

    show(x)

And Much More
=============

While avoiding a few extra characters of typing and a little extra
program complexity is nice (very nice, actually), ``show`` does much
more. As just a taste, ``show.changed()`` displays local values that have
changed since it was last run::

    def f():
        x = 4
        show.changed()
        x += 1
        retval = x * 3
        show.changed()
        return retval

When run will display::

    x: 4
    x: 5  retval: 15

Decorate a function with ``@show.inout`` and it will show you the
input parameters as the function is called, and then the return
value later.::

    @show.inout
    def g(a):
        b = 3
        a += b
        show.changed()
        return a

    g()

Displays::

    g(a=4)
    a: 7  b: 3
    g(a=4) -> 7

And of course ``show`` does normal output too, just like
`say <https://pypi.python.org/pypi/say>`_ (with all of its
high-level text formatting)::

    wizard = "Gandalf"
    show("You have no power here, {wizard}!")

Prints::

    You have no power here, Gandalf!

Just like you knew it would.

Long story short, ``show`` is working toward being a full-featured
debugging companion that prints the maximum amount of useful information
with the minimum amount of fuss.

For this and much more, see `the full documentation at Read the Docs
<http://show.readthedocs.org/en/latest/>`_.

.. warning:: There are known issues about running this on Python 2.6 and 3.5,
    and on Windows. Also, when evaluating this module's usefulness, do so
    in a program file that you run, not interactively. It's much
    more robust and effective
    in standard, non-interactive execution, given some challenges it
    currently faces
    getting cogent "where am I?" information from interactive interpreters.


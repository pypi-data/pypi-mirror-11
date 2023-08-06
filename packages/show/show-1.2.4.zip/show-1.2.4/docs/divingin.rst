Diving In
=========

Sometimes programs print so that users can see things, and sometimes they print
so that developers can. ``show()`` is for developers, helping
rapidly print the current state of variables. A simple invocation::

    show(x)

replaces require the craptastic
repetitiveness of::

    print "x: {0}".format(x)

If you'd like to see where the data is being produced,::

    show.set(where=True)
    show(d)

will turn on location reporting, such as::

    __main__():21:   d: 'this'

The ``where`` property, along with most every option, can be set
permanently, over the scope of a ``where`` block, or on
a call-by-call basis.
``show`` is built atop the `options <http://pypi.python.org/pypi/options>`_ module
for configuration management, and the output management of
`say <http://pypi.python.org/pypi/say>`_. All ``say`` options are available. If you
``show()`` a literal string, it will be interpolated as it would be in ``say``::

    show("{n} iterations, still running")

yields something like::

    14312 iterations, still running

But::

    s = '{n} iterations'
    show(s)

yields::

    s: '{n} iterations'

See ``say`` `say <http://pypi.python.org/pypi/say>`_ for additional detail on its
operation. ``show`` directly supports many ``say`` methods such as
``blank_lines``, ``hr``, ``sep``, and ``title`` which are meant to simplify
and up-level common formatting tasks.



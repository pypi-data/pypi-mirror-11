How Things Are Shown
====================

By default, ``show`` uses Python's ``repr()`` function to format
values. You may prefer some other kind of representation or formatting,
however. For example, the ``pprint`` module pretty-prints data structures.
You can set it to be the default formatter::

    from pprint import pformat
    show.set(fmtfunc=pformat)

Or to configure separate data and
code formatters::

    show.set(fmtfunc=lambda x: pformat(x, indent=4, width=120, depth=5))
    show.set(fmtcode=lambda x: highlight(x, ...))

As a convenience, the ``show.prettyprint()`` configures
``pygments`` and
``pprint`` in concert to more attractively display text on
ANSI terminals. Just run it once after importing ``show``.
It also takes ``indent``, ``depth``, and ``width`` options
for ``pformat`` and the ``style`` (style name) option for ``pygments``.
Some style names to try::

    # monokai manni rrt perldoc borland colorful default
    # murphy vs trac tango fruity autumn bw emacs vim pastie
    # friendly native



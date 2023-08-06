Wax On, Wax Off
===============

Often it's convenient to only display debugging information under some conditions,
but not others,
such as when a ``debug`` flag is set. That often leads to multi-line conditionals
such as::

    if debug:
        print "x:", x, "y:", y, "z:", z

With ``show`` it's a bit easier. There's a keyword argument, also called
``show``, that controls whether anything is shown. If it's truthy, it shows;
falsy, ad it doesn't::

    show(x, y, z, show=debug)

You can set the show flag more globally::

    show.set(show=False)

You can also make multiple ``show`` instances that can be separately controlled::

    show_verbose = show.clone()
    show_verbose.set(show=verbose_flag)
    show_verbose(x, y, z)

For a more fire-and-forget experience, try setting visibility with a lambda
parameter::

    debug = True
    show.set(show=lambda: debug)

Then, whenever ``debug`` is truthy, values will be shown. When ``debug`` is
falsy, values will not be shown.

When you really, truly want ``show``'s output to
disappear, and want to minimize
overhead, but don't want to
change your source code (lest you need those debug printing statements again
shortly), try::

    show = noshow

This one line will replace the ``show`` object (and any of its clones) with
parallel ``NoShow`` objects that simply don't do anything or print any output.

.. note:: This assignment should be done in a global context. If done inside a
    function, you'll need to add a corresponding ``global show`` declaration.

As an alternative, you can::

    from show import show
    from show import noshow as show

Then comment out the``noshow`` line for debugging, or the ``show`` line for production
runs.

.. note:: A little care is required to configure global non-showing behavior
    if you're using ``show``'s function decorators such as ``@show.inout``.
    Decorators are evaluated earlier in program execution than the "main flow"
    of program execution, so it's a good idea to define the lambda or ``noshow``
    control of visibility at the top of your program.


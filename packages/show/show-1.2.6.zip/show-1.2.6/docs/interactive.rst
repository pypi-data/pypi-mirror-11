Interactive Limitations
=======================

``show`` has experimental support for interactive Python and iPython. It works
well at the interactive prompt, and within imported modules. It cannot, however,
be used within functions and classes defined within the interactive session.
This is a result of how Python supprots--or fails to support--introspection for
interactively defined code. Whether this is a hard limit, or something that can
be worked around over time, remains to be seen. (See e.g. `this discussion
<http://stackoverflow.com/questions/13204161/how-to-access-the-calling-source-line-from-interactive-shell>`_).

Python under Windows does not support readline the same way it is supported
on Unix, Linux, and Mac OS X. Experimental
support is provided for the use of ``pyreadline`` under Windows to correct
this variance. This feature is yet untested. Works/doesn't work reports welcome!

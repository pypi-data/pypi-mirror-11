Titles and Horizontal Rules
===========================

``say`` defines a few convenience formatting functions::

    say.title('Errors', sep='-')
    for i,e in enumerate(errors, start=1):
        say("{i:3}: {e['name'].upper()}")

might yield::

    --------------- Errors ---------------
      1: I/O ERROR
      2: COMPUTE ERROR

A similar method ``hr`` produces just a horizontal line ("rule"), like
the HTML ``<hr>`` element. For either, one can optionally
specify the width (``width``), character repeated to make the line (``sep``),
and vertical separation/whitespace above and below the item (``vsep``).
Good options for the separator might be be '-', '=', or parts of the `Unicode
box drawing character set <http://en.wikipedia.org/wiki/Box-drawing_character>`_.

A final method, ``sep``, creates a short left-aligned bar with optional
following text. It's useful for creating logical subsections.::

    say.sep("coffee")
    say("I prefer coffee")
    say.sep("tea", sep="=", width=4, vsep=(1,0))
    say("I prefer tea")

Yields::

    -- coffee
    I prefer coffee

    ==== tea
    I prefer tea

You can even define reusable styles for separators (and other say calls)::

    tilde_sep = dict(sep="~", width=4, vsep=(1,0))
    say.sep("pass one", **tilde_sep)

Yields::

    ~~~~ pass one



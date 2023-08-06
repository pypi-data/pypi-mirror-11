Vertical Spacing
================

You don't need to add explicit
newline characters here and there to achieve good
vertical spacing.  ``say.blank_lines(n)`` emits n blank lines. And just
about every ``say`` call also supports a ``vsep`` (vertical separation)
parameter.::

    say('TITLE', vsep=(2,0)        # add 2 newlines before (none after)
    say('=====', vsep=(0,2))       # add 2 newlines after (none before)
    say('something else', vsep=1)  # add 1 newline before, 1 after


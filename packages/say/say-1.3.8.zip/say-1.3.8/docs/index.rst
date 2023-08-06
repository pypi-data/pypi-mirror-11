say
===

It's been *forty five years* since ``C`` introduced ``printf()`` and the basic
formatted printing of positional parameters. Isn't it time for an upgrade?
**You betcha!**

``say`` evolves Python's ``print``
statement/function, ``format`` function/method, and ``%`` string
interpolation operator with simpler, higher-level facilities. For example,
it provides direct template formatting:

* DRY, Pythonic, inline string templates that piggyback
  Python's well-proven ``format()`` method, syntax, and underlying engine.
* A single output mechanism that works the same way across
  Python 2 or Python 3.
* A companion ``fmt()`` object for string formatting.
* Higher-order line formatting such as line numbering,
  indentation, and line-wrapping built in. You can get substantially
  better output
  formatting with almost no additional code.
* Convenient methods for common formatting items such as titles, horizontal
  separators, and vertical whitespace.
* Easy styled output, including ANSI colors and user-defined styles
  and text transforms.
* Easy output to one or more files, without additional code or complexity.
* Super-duper template/text aggregator objects for easily building,
  reading, and writing multi-line texts.


Usage
=====

::

    from say import *

    x = 12
    nums = list(range(4))
    name = 'Fred'

    say("There are {x} things.")
    say("Nums has {len(nums)} items: {nums}")
    say("Name: {name!r}")

yields::

    There are 12 things.
    Nums has 4 items: [0, 1, 2, 3]
    Name: 'Fred'

Or if you want the resulting string, rather than to print the string::

    >>> fmt("{name} has {x} things and {len(nums)} numbers.")
    'Fred has 12 things and 4 numbers.'

At this level, ``say`` is basically a simpler, nicer recasting of::

    from __future__ import print_function

    print("There are {0} things.".format(x))
    print("Nums has {0} items: {1}".format(len(nums), nums))
    print("Name: {0!r}".format(name))
    s = "{0} has {1} things and {2} numbers.".format(name, x, len(nums))

(The ``import`` and
numerical sequencing of ``{}`` format specs is required to make pure-Python
code work correctly from Python 2.6 forward from
a single code base.)

But ``say`` and ``fmt`` read so much nicer! They are clear, simplem
and direct, and don't separate the place where the value
should appear from the value.

Full expressions are are supported within the format braces (``{}``). Whatever
variable names or expressions are found therein will be evaluated in the context
of the caller.

The more items that are being printed, and the complicated the ``format``
invocation, the more valuable this simple inline specification becomes.

But ``say`` isn't just replacing positional templates with inline templates.
It also works in a variety of ways to up-level the output-generation task.
For example::

    say.title('Discovered')
    say("Name: {name:style=blue}", indent='+1')
    say("Age:  {age:style=blue}", indent='+1')

.. image:: http://content.screencast.com/users/jonathaneunice/folders/Jing/media/81bf4738-c875-4998-82ac-a91d211d000b/00000745.png
    :align: left

Prints a nicely formatted text block, with a proper title and indentation,
and just the variable information in blue.


Indentation and Wrapping
========================

Indentation is a common way to display data hierarchically. ``say`` will
help you manage it. For example::

    say('ITEMS')
    for item in items:
        say(item, indent=1)

will indent the items by one indentation level (by default, each indent
level is four spaces, but
you can change that with the ``indent_str`` option).

If you want to change the default indentation level::

    say.set(indent=1)      # to an absolute level
    say.set(indent='+1')   # strings => set relative to current level

    ...

    say.set(indent=0)      # to get back to the default, no indent

Or you can use a ``with`` construct::

    with say.settings(indent='+1'):
        say(...)

        # anything say() emits here will be auto-indented +1 levels

    # anything say() emits here, after the with, will not be indented +1

.. note:: If using a string to indicate relative indent levels offends your sense of
    dimensionality or strict typing, there is a class ``Relative`` that does the same
    thing in a more formal way. ``indent='+2'`` and ``indent=Relative(+2)`` are identical.

If you have a lot of data or text to print, and it would normally create
super-long, difficult-to-read lines, you can easily wrap it::

    say("This is a really long...blah blah blah", wrap=40)

Will automatically wrap the text to the given width
using Python's standard ``textwrap`` module.
Feel free to use indentation and wrapping together.

Prefixes and Suffixes
=====================

Every line can be given a prefix or suffix, if desired. For example::

    with say.settings(prefix='> '):
        say('this')
        say('that')

Will give what text email and Markdown consider a quoted block look::

    > this
    > that

Or if you'd like some text to be quoted with blue quotes::

    say(text, prefix=styled('> ', 'blue'))

And if you like your output numbered::

    say.set(prefix=numberer())
    say('this\nand\nthat')

yields::

      1: this
      2: and
      3: that

You can instantiate different numberers for different files, and if you
like, use the ``start`` keyword argument to start a ``numberer`` on
a designated value.

The Value Proposition
=====================

While it's easy enough to add a few spaces to the format string of any ``print``
statement or function in order to achieve a little indentation, it's easy to
mistakenly type too many or too few spaces, or to forget to type them in some
format strings. If you're indenting strings that themselves may contain
multiple lines, the simple ``print`` approach breaks because it won't take
multi-line strings into account. Nor will it be integrated with line wrapping
or numbering or other formatting you also want.

``say``, however, simply and correctly handles these combined formatting
operations. Harder cases like multi-line strings are just as nicely and well
indented as simple ones--something not otherwise easily accomplished without
adding gunky, complexifying string manipulation code to every place in your
program that prints anything.

This starts to illustrate ``say``'s "do the right thing" philosophy. So many
languages' printing and formatting functions "output values" at a low level.
They may format basic data types, but they don't provide straightforward ways to
do neat text transformations that rapidly yield correct, attractively-formatted
output. ``say`` does. Over time, ``say`` will provide even more high-level
formatting options. For now: indentation, wrapping, and line numbering.

.. note:: If you do find any errors in the way ``say`` handles formatting operations,
    `there's an app for that <https://bitbucket.org/jeunice/say/issues>`_. Let's fix
    them once, in a common place, in reusable code--not spread around many different programs.

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

Colors and Styles
=================

``say`` has built-in support for style-driven formatting. By default,
ANSI terminal colors and styles are automagically supported.

::

    answer = 42

    say("The answer is {answer:style=bold+red}")

This uses the `ansicolors <https://pypi.python.org/pypi/ansicolors>`_
module, though with a slightly more permissive syntax. Available colors are
'black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', and 'yellow'.
Available styles are 'bold', 'italic', 'underline', 'blink', 'blink2',
'faint', 'negative', 'concealed', and 'crossed'. These styles can be
combined with a ``+`` or ``|`` character. Note, however, that not all styles
are available on every terminal.

.. note:: When naming a style within the template braces (``{}``) of format strings, you can quote the style name or not. ``fmt("{x:style=red+bold}")`` is equivalent to ``fmt("{x:style='red+bold'}")``.

You can define your own styles::

    say.style(warning=lambda x: color(x, fg='red'))

Because styles are defined through executables (lambdas, usually), they can
include decisions or text transformations of arbitrary complexity.
For example::


    say.style(redwarn=lambda n: color(n, fg='red', style='bold') if int(n) < 0 else n)
    ...
    say("Result: {n:style=redwarn}")

That will display the number ``n`` in bold red characters, but only if it's value is
negative. For positive numbers, ``n`` is displayed normally.

Or define a style where a message is surrounded by red stars::

    say.style(stars=lambda x: fmt('*** ', style='red') + \
                              fmt(x,      style='black') + \
                              fmt(' ***', style='red'))
    say.style(redacted=lambda x: 'x' * len(x))

    message = 'hey'
    say(message, style='stars')
    say(message, style='redacted')

Yields::

    *** hey ***
    xxx

(with red stars)

.. note:: Style defining lambdas (or functions) take string arguments. If the string is logically a number, it must be then cast into an ``int``, ``float``, or whatever. The code must ultimate return a string.

You can also apply a style to the entire contents of a ``say`` or ``fmt`` invocation::

    say("There is green everywhere!", style='green|underline')

While the goal of ``say`` is to have correct behavior under absolutely all
combinations of text styling, coloring, indentation, numbering, and so on, be
aware that the coloring/styling is relatively new, has limited tests and
documentation to date, and is still evolving. One known bug attends ``say``'s
use of Python's ``textwrap`` module, which is not savvy to ANSI-terminal control
codes; text that includes control codes and is wrapped is currently likely to
wrap in the wrong place. Enclosing one bit of colored text inside another bit of
colored text is not as easy as it could be. Finally, style definitions are
idiosyncratically shared across instances. That said, some fairly complex
invocations already work quite nicely. Try, e.g.::

    say.set(prefix=numberer(template=color('{n:>3}: ', fg='blue')), \
            wrap=40)
    say('a long paragraph...with gobs of text', style='red')

This correctly puts the line numbers in blue, wraps the lines to 40 characters,
and puts the text in red. (The ``textwrap`` collision with control characters
is avoided here because the wrapped text is pure, and the control codes for
red styling are added after wrapping.)

Styled formatting is an extremely powerful approach, giving the
same kind of flexibility and abstraction seen for styles in word processors and
CSS-based Web design. It will be further developed.
Plans already include replacing ``textwrap`` with an ANSI-savvy text wrapping
module, providing simpler ways to state complex formatting, and mechanisms
to auto-map styles into HTML output.

Where You Like
==============

``say()`` writes to a list of files--by default just ``sys.stdout``. But
with one simple configuration call, it will write to different--even
multiple--files::

    import sys
    from say import say

    say.set(files=[sys.stdout, "report.txt"])
    say(...)   # now prints to both sys.stdout and report.txt

This has the advantage of allowing you to both capture and see program output,
without changing any code (other than the config statement). You can also define
your own targeted ``Say`` instances::

    import sys
    from say import say

    err = say.clone(files=[sys.stderr, 'error.txt'])
    err("Failed with error {errcode}")  # writes in both places
    say("something else")   # independent of err

When You Like
=============

If you want to stop printing for a while::

    say.set(silent=True)  # no printing until set to False

Or transiently::

    say(...stuff..., silent=not verbose) # prints iff bool(verbose) is True

Of course, you don't have to print at all.
``fmt()`` works exactly like ``say()`` and inherits most of its options,
but doesn't print. (The ``C`` analogy: ``say`` **:** ``fmt`` **::** ``printf``
**:** ``sprintf``.)

Encodings
=========

Character encodings remain a fractious and often exasperating part of IT.
``say()`` and ``fmt()`` try to avoid this by working with Unicode strings. In
Python 3, all strings are Unicode strings, and output is by default UTF-8
encoded. Yay!

In Python 2, we try to maintain the same environment. If a template or input
string is *not* of type ``unicode``, please include only ASCII characters, not
encoded bytes from UTF-8 or whatever. If you don't do this, any trouble results
be on your head. If ``say`` opens a file for you (e.g. with ``setfiles()``), it
uses ``io.open()`` to inherit its default encoding to UTF-8. If you have ``say``
write to a file that you've opened, you should similarly use ``io.open()`` or
another mechanism that transparently writes to a proper encoding.

Non-Functional Invocation
=========================

For those who don't want to always and forever surround "print statements" with
the Python 3-style function parentheses, the ``>`` operator is
provided as an experimental, non-functional way to print. The following
are identical::

    say> "{user.id}: {user.username}"
    say("{user.id}: {user.username}")

You can name as many values as you like in the format string, but there can
only be one format string, and no options. If you need to ``say`` multiple values,
or say them with statement-specific options, you must use the functional syntax.

Text and Templates
==================

Often the job of output is not about individual text lines, but about creating
multi-line files such as scripts and reports. This often leads away from standard
output mechanisms toward template packages, but ``say`` has you covered here as
well.

::

    from say import Text

    # assume `hostname` and `filepath` already defined

    script = Text()
    script += """
        !#/bin/bash

        # Output the results of a ping command to the given file

        ping {hostname!r} >{filepath!r}
    """

    script.write_to("script.sh")

Then ``script.sh`` will contain::

    !#/bin/bash

    # Output the results of a ping command to the given file

    ping 'server1234.example.com' >'ping-results.txt'

``Text`` objects are basically a list of text lines. In most cases, when you add
text (either as multi-line strings or lists of strings), ``Text`` will
automatically interpolate variables the same way ``say`` does. One can
simply ``print`` or
``say`` ``Text`` objects, as their ``str()`` value is the full text you would
assume. ``Text`` objects have both ``text`` and ``lines`` properties which
can be either accessed or assigned to.

``+=`` incremental assignment
automatically removes blank starting and ending lines, and any whitespace prefix
that is common to all of the lines (i.e. it will *dedent* any given text).
This ensures you don't need to give up
nice Python program formatting just to include a template.

While ``+=`` is a handy way of incrementally building text, it
isn't strictly necessary in the simple example above; the
``Text(...)`` constructor itself accepts a string or set of lines.

Other in-place operators are: ``|=`` for adding text while preserving leading white
space (no dedent) and ``&=`` adds text verbatim--without dedent or string
interpolation.

One can ``read_from()`` a file (appending the contents of the file to the given
text object, with optional interpolation and dedenting). One can also
``write_to()`` a file. Use the ``append`` flag if you wish to add to rather than
overwrite the file of a given name, and you can set an output encoding if you
like (``encoding='utf-8'`` is the default).

So far we've discussed ``Text`` objects almost like strings, but they also act
as lists of individual lines (strings). They are, for example,
indexable via ``[]``, and they are iterable.
Their ``len()`` is the number of lines they contain. One can
``append()`` or ``extend()`` them with one or multiple strings, respectively.
``append()`` takes a keyword parameter ``interpolate`` that controls whether
``{}`` expressions in the string are interpolated. ``extend()`` additionally takes
a ``dedent`` flag that, if true, will
automatically remove blank starting and ending lines, and any whitespace prefix
that is common to all of the lines.

If ``t`` is a ``Text`` instance, ``str(t)`` will be the full string representing it.
If you wish to move from multiple lines to a single-line, joined string, ``' '.join(t)``
does the trick.

``Text`` objects, unlike strings, are mutable. The ``replace(x, y)`` method will
replace all instances of ``x`` with ``y`` *in situ*. If given just one argument,
a ``dict``, all the keys will be replaced with their corresponding values.

``Text`` doesn't have the full set of text-onboarding options seen in `textdata
<http://pypi.python.org/pypi/textdata>`_, but it should suit many circumstances.
If you need more, ``textdata`` can be used alongside ``Text``.

Finally, it's possible to use a ``Text`` object like a file and write to it.
So::

    t = Text()
    say.set(files=[sys.stdout, t])

    say('something')

will now append each thing said to both ``sys.stdout`` and ``t``.

There is a related class ``Template`` that does not interpolate its
format variables when constructed, but rather when explicitly rendered. This
suits certain form-filling operations::

    t = Template("Dear {name},\n\nWelcome to our club!\n")
    for name in 'Joe Jane Jeremey'.split():
        print t.render()


Iterpolators and Exceptions
===========================

You may want to write your own functions that take strings
and interpolate ``{}``
format templates in them. The easy way is::

    from say import caller_fmt

    def ucfmt(s):
        return caller_fmt(s).upper()

If ``ucfmt()`` had used ``fmt()``, it would not have worked. ``fmt()`` would
look for interpolating values within the context of ``ucfmt()`` and, not finding
any, probably raised an exception. But using ``caller_fmt()`` it looks into the
context of the caller of ``ucfmt()``, which is exactly where those values would
reside. *Voila!*

And example of how this can work--and a useful tool in its own right--is ``FmtException``.
If you want to have comprehensible error messages when something goes wrong, you
could use ``fmt()``::

    if bad_thing_has_happened:
        raise ValueError(fmt("Parameters {x!r} or {y!r} invalid."))

But if you define your own exceptions, consider subclassing ``FmtException``::

    class InvalidParameters(FmtException, ValueError):
        pass

    ...

    if bad_thing_has_happened:
        raise InvalidParameters("Parameters {x!r} or {y!r} invalid.")

You'll save a few characters, and the code will be simpler and more comprehensible.

Python 3
========

Say works virtually the same way in Python 2 and Python 3. This can simplify
software that should work across the versions, without the hassle
of ``from __future__ import print_function``.

``say`` attempts to mask some of the quirky complexities of the 2-to-3 divide,
such as string encodings and codec use. In general, things work best if
you use Unicode strings any time you need to use non-ASCII characters.
In Python 3, this is automatic.

Alternatives
============

* `ScopeFormatter <http://pypi.python.org/pypi/ScopeFormatter>`_
  provides variable interpolation into strings. It is amazingly
  compact and elegant. Sadly, it only interpolates Python names, not full
  expressions. ``say`` has full expressions, as well as a framework for
  higher-level printing features beyond ``ScopeFormatter``'s...um...scope.

* `interpolate <https://pypi.python.org/pypi/interpolate>`_ is
  similar to ``say.fmt()``, in that it can
  interpolate complex Python expressions, not just names.
  Its ``i % "format string"`` syntax is a little odd, however, in
  the way that it re-purposes Python's earlier ``"C format string" % (values)``
  style ``%`` operator. It also depends on the native ``print`` statement
  or function, which doesn't help bridge Python 2 and 3.

* Even simpler are invocations of ``%`` or ``format()``
  using ``locals()``. E.g.::

       name = "Joe"
       print "Hello, %(name)!" % locals()
       # or
       print "Hello, {name}!".format(**locals())

  Unfortunately this has even more limitations than ``ScopeFormatter``: it
  only supports local variables, not globals or expressions. And the
  interpolation code seems gratuitous. Simpler::

      say("Hello, {name}!")

Notes
=====

* The ``say`` name was inspired by Perl's `say <http://perldoc.perl.org/functions/say.html>`_,
  but the similarity stops there.

* Automated multi-version testing managed with the wonderful `pytest
  <http://pypi.python.org/pypi/pytest>`_ and `tox
  <http://pypi.python.org/pypi/tox>`_. Successfully packaged for, and
  tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
  and 3.4, as well as PyPy 2.6.0 (based on 2.7.9) and PyPy3 2.4.0 (based on
  3.2.5). Should run fine on Python 3.5, though py.test is broken on its
  pre-release iterations.

* ``say`` has greater ambitions than just simple template printing. It's
  part of a larger rethinking of how output should be formatted. `show
  <http://pypi.python.org/pypi/show>`_` and ``Text`` are other
  down-payments on this larger vision. Stay tuned.

* In addition to being a practical module in its own right, ``say`` is
  testbed for `options <http://pypi.python.org/pypi/options>`_, a package
  that provides high-flexibility option, configuration, and parameter
  management.

* Those who appreciate the simple output this module enables may also
  like `quoter <http://pypi.python.org/pypi/quoter>`_, a related effort
  to make text wrapping and sequence joining easy and powerful.

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
  `@jeunice on Twitter <http://twitter.com/jeunice>`_
  welcomes your comments and suggestions. If you're using ``say`` in your own
  work, drop me a note and tell me how you're using it, how you like it,
  and what you'd like to see!

To-Dos
======

* Use a text wrapping module that is fully cognient of ANSI escape codes.
* Further formatting techniques for easily generating HTML output and
  formatting non-scalar values.
* Provide code that allows ``pylint`` to see that variables used inside
  the ``say`` and ``fmt`` format strings are indeed thereby used.

Installation
============

To install or upgrade to the latest version::

    pip install -U say

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade say

(You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)

Funding
=======

If you find this useful, consider contributing to fund its development:

.. image:: https://img.shields.io/gratipay/jeunice.svg
    :target: https://www.gittip.com/jeunice/


.. toctree::
   :maxdepth: 2

   CHANGES

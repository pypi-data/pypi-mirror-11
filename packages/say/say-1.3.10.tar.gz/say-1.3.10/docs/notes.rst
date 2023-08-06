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

* If you find ``say`` useful, consider buying me a pint and a nice
  salty pretzel. |funding|

.. |funding| image:: https://img.shields.io/gratipay/jeunice.svg
    :target: https://www.gittip.com/jeunice/

To-Dos
======

* Use a text wrapping module that is fully cognient of ANSI escape codes.
* Further formatting techniques for easily generating HTML output and
  formatting non-scalar values.
* Provide code that allows ``pylint`` to see that variables used inside
  the ``say`` and ``fmt`` format strings are indeed thereby used.


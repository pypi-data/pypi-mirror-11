Interstat
=========

An HTML formatter for IRC log files.
Currently, only the format used by Omnipresence_ is supported; look in
``interstat.formats`` for an idea of how to add more.

.. _Omnipresence: https://github.com/kxz/omnipresence

Install it with::

    $ pip install interstat

Then run::

    $ interstat LOGFILE HTMLFILE

If you want to change the generated HTML or CSS, copy the files in the
``interstat/templates`` directory that you want to override, make your
changes, and run::

    $ interstat --template-dir my-templates/ LOGFILE HTMLFILE

For more options, try::

    $ interstat --help

Interstat also provides a Python API, in case that's more your thing:

>>> import interstat
>>> # Convert an entire log file:
>>> interstat.file_as_html(open('irc.log'), 'omnipresence')
>>> # Or just some text with embedded mIRC formatting codes:
>>> interstat.line_as_html('\x02Bold\x02 and \x1Funderlined\x1F, oh my!')

Report bugs and make feature requests on `Interstat's GitHub project
page <https://github.com/kxz/interstat>`_.

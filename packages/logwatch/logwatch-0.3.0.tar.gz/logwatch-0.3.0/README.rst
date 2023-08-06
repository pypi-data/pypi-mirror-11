logwatch
========

Email alerts when tail -1 of log file does not match regex

Installation
------------

From the project root directory::

    $ python setup.py install

Usage
-----

Watch file at /var/log/nginx/access.log using configured regex in ~/.watcher.yml::

    $ logwatch /var/log/nginx/access.log

Watch file, sleeping for 60 seconds, with verbosity to print regex matches

    $ logwatch /var/log/nginx/access.log -S 60 -v

Watch with special regex and print groups timestamp and message, ignoring empty file

    $ logwatch /var/log/foo.log -r '\[(?P<timestamp>\d+)\] (?P<message>.*)' -e

Use --help/-h to view info on the arguments::

    $ logwatch --help

Release Notes
-------------

:0.1.0:
    Alpha runs and works
:0.0.1:
    Project created

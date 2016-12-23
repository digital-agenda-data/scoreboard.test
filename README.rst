===============
scoreboard.test
===============

Selenium based automated testing.


Installation
------------
This package requires **Python 3.5**!
::

    $ virtualenv scoreboard
    $ cd scoreboard
    $ source ./bin/activate
    $ pip install -U https://github.com/eaudeweb/scoreboard.test/archive/master.zip
    $ scoreboard-test -h



Usage
-----

To run the ``indicators``, ``charts`` and ``dataset`` tests in Firefox,
specifying the path to ``geckodriver`` at the default ``1024x768`` resolution: ::

    $ scoreboard-test -v -B firefox -P /usr/bin/geckodriver https://digital-agenda-data.eu indicators charts dataset


To run all tests in phantomjs in glorious 4K resolution: ::

    $ scoreboard-test -v -B phantomjs -P /usr/bin/phantomjs -sw 3840 -sh 2160 https://digital-agenda-data.eu

Failed tests and tests that encounter an error will save a screenshot in the current working directory.


Contribute
----------

- Issue Tracker: https://github.com/eaudeweb/scoreboard.test/issues
- Source Code: https://github.com/eaudeweb/scoreboard.test
- Documentation: https://github.com/eaudeweb/scoreboard.test/wiki


License
-------

The project is licensed under the GPLv2.

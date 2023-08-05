===============================
simple-pypi-statistics
===============================

.. image:: https://travis-ci.org/benjaoming/simple-pypi-statistics.svg
    :target: https://travis-ci.org/benjaoming/simple-pypi-statistics

.. image:: https://img.shields.io/pypi/v/simple-pypi-statistics.svg
        :target: https://pypi.python.org/pypi/simple-pypi-statistics


API and commandline for fetching simple statistics from PyPi's API

* Free software: GPLv2

Usage
-----

Run ``simple-pypi-statistics`` to show usage::

    simple-pypi-statistics
    
    Usage:
      simple-pypi-statistics [options] [verbose|json] <pypi-package>...
      simple-pypi-statistics (-h | --help)
      simple-pypi-statistics --version
    
    Options:
      --no-honeypot   Do not use honeypot for correcting bot/mirror pollution
                      [default: False]
      -h --help       Show this screen.
      --version       Show version.
    
    Examples:
      simple-pypi-statistics docopt  # Outputs everything about docopt
      simple-pypi-statistics docopt==0.1  # Outputs a specific version
      simple-pypi-statistics json docopt==0.1  # In JSON!
    
    Credits:
      Benjamin Bach -- updated script with honey pot corrections
      Alex Clark -- for making vanity, which this script is based on


Features
--------

* verbose output
* JSON output
* functions in api for direct access


Honey pot
---------

A bogus project on PyPi is used to track garbage stats. To assure that things are
working, consider that the grand total of downloads for that project is actually
also ``0``::

    python3 -m simple_pypi_statistics python-bogus-project-honeypot
    python-bogus-project-honeypot-1438620531.16.tar.gz    2015-08-03           12
    python-bogus-project-honeypot-1438619971.82.tar.gz    2015-08-03          -12
    -----------------------------------------------------------------------------
    No downloads for python-bogus-project-honeypot.


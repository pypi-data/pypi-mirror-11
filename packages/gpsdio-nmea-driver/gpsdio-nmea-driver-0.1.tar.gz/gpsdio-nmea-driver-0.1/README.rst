==================
gpsdio-nmea-driver
==================

An **experimental** gpsdio driver for parsing NMEA sentences directly into GPSd messages with `libais <https://github.com/schwehr/libais>`_.

.. image:: https://travis-ci.org/SkyTruth/gpsdio-nmea-driver.svg?branch=master
    :target: https://travis-ci.org/SkyTruth/gpsdio-nmea-driver

.. image:: https://coveralls.io/repos/SkyTruth/gpsdio-nmea-driver/badge.svg?branch=master
    :target: https://coveralls.io/r/SkyTruth/gpsdio-nmea-driver


Installation
------------

**NOTE:** This driver is experimental and requires an unreleased version of ``libais`` and ``gpsdio``.

With pip:

.. code-block:: console

    $ pip install git+git://github.com/schwehr/libais.git --upgrade
    $ pip install gpsdio-nmea-driver

From source:

.. code-block:: console

    $ git clone https://github.com/SkyTruth/gpsdio
    $ cd gpsdio-nmea-driver
    $ python setup.py install
    $ pip install git+git://github.com/schwehr/libais.git --upgrade
    $ pip install git+git://github.com/schwehr/libais.git --upgrade


Developing
----------

.. code-block:: console

    $ git clone https://github.com/SkyTruth/gpsdio-nmea-driver.git
    $ cd gpsdio-nmea-driver
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -e .\[dev\]
    $ py.test tests --cov gpsdio-nmea-driver --cov-report term-missing


Changelog
---------

See ``CHANGES.md``


License
-------

See ``LICENSE.txt``

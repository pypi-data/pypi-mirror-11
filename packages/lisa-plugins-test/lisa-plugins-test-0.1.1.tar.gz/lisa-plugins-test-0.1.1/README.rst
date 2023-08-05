lisa-plugins-test
======================================

|build-status-image| |pypi-version|

Overview
--------

Test plugin

Requirements
------------

-  Python (2.7, 3.4)
-  Django (1.8)
-  Django REST Framework (3.0, 3.1)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install lisa-plugins-test

Example
-------

TODO: Write example.

Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/Seraf/lisa-plugins-test.svg?branch=master
   :target: http://travis-ci.org/Seraf/lisa-plugins-test?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/lisa-plugins-.svg
   :target: https://pypi.python.org/pypi/lisa-plugins-test

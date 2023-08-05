===========
Clustercron
===========

.. image:: https://badge.fury.io/py/clustercron.svg
    :target: http://badge.fury.io/py/clustercron

.. image:: https://readthedocs.org/projects/clustercron/badge/?version=latest
    :target: http://clustercron.readthedocs.org/en/latest/

.. image:: https://travis-ci.org/maartenq/clustercron.svg?branch=master
    :target: https://travis-ci.org/maartenq/clustercron

.. image:: https://codecov.io/github/maartenq/clustercron/coverage.svg?branch=master
        :target: https://codecov.io/github/maartenq/clustercron?branch=master


Clustercron is cronjob wrapper that tries to ensure that a script gets run only
once, on one host from a pool of nodes of a specified loadbalancer.

Supported load balancers (till now):

    * AWS Elastic Load Balancing

* PyPi: https://pypi.python.org/pypi/clustercron
* GitHub: https://github.com/maartenq/clustercron
* Documentation: https://clustercron.readthedocs.org/en/latest/
* Travis CI: https://travis-ci.org/maartenq/clustercron
* Codecov: https://codecov.io/github/maartenq/clustercron
* Free software: BSD license




History
=======

0.3.4 (2015-07-12)
-----------------------

* Correction in docs/usage.rst


0.3.3 (2015-07-12)
-----------------------

* Remove :ref: tag from README.rst (for formatting on PyPi)


0.3.2 (2015-07-12)
-----------------------

* Fix mock requirements in tox.ini (mock 1.1.1 doesn't work with Python 2.6)


0.3.1 (2015-06-28)
-----------------------

* First release (beta status)


0.3.0 (2015-06-28)
-----------------------

* First release


0.3.0.dev2 (2015-06-21)
-----------------------

* First real working version for ELB


0.3.0.dev1 (2015-06-17)
-----------------------

* First working version for ELB

0.2.0.dev2 (2015-05-25)
-----------------------

* In Development stage 1
* Removed HAproxy for now.


0.1.3 (2015-05-22)
---------------------

* Refactor command line argument parser


0.1.2 (2015-03-28)
---------------------

* More test for commandline
* Travis stuff


0.1.0 (2015-01-23)
---------------------

* First release on PyPI.



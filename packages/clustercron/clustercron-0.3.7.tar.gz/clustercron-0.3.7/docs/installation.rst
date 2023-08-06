Installation
============

Virtualenv
----------

* Make virtual environment::

    $ virtualenv /<path>/<to>/<virtualenv_name>


* Activate virtual environment::

    $ source /<path>/<to>/<virtualenv_name>/bin/activate


* Install *clustercron*::

    (<virtualenv_name>)$ pip install clustercron



Boto Config
-----------

For Clustercron ELB a `Boto Config`_ is needed.

See :ref:`clustercron-elb` for more information.

.. _Boto Config: http://boto.readthedocs.org/en/latest/boto_config_tut.html

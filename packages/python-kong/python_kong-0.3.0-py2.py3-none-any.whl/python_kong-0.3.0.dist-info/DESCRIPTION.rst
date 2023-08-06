===========
python-kong
===========

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |circleci| |coveralls| |scrutinizer|
    * - package
      - |version| |downloads| |wheel|
    * - compatibility
      - |pyversions| |implementation|

.. |docs| image:: https://readthedocs.org/projects/python-kong/badge/?style=flat
    :target: https://readthedocs.org/projects/python-kong
    :alt: Documentation Status

.. |circleci| image:: https://img.shields.io/circleci/project/vikingco/python-kong.svg?style=flat&label=CircleCI
    :alt: CircleCI Build Status
    :target: https://circleci.com/gh/vikingco/python-kong

.. |coveralls| image:: http://img.shields.io/coveralls/vikingco/python-kong/master.svg?style=flat&label=Coveralls
    :alt: Coverage Status
    :target: https://coveralls.io/github/vikingco/python-kong

.. |version| image:: http://img.shields.io/pypi/v/python-kong.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/python-kong

.. |downloads| image:: http://img.shields.io/pypi/dm/python-kong.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/python-kong

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/vikingco/python-kong/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/vikingco/python-kong/

.. |wheel| image:: https://img.shields.io/pypi/wheel/python-kong.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/python-kong

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/python-kong.svg?style=flat
    :alt: Supported python versions
    :target: https://pypi.python.org/pypi/python-kong

.. |implementation| image:: https://img.shields.io/pypi/implementation/python-kong.svg?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/python-kong

A Python client for the Kong API (https://getkong.org/)

* Free software: BSD license

Installation
============

::

    pip install python-kong

Documentation
=============

https://python-kong.readthedocs.org/

Development
===========

To run the all tests run::

    tox


Changelog
=========

0.3.0 (2015-09-22)
------------------

* Updated library again to be compatible with Kong 0.5.x (WARNING: Not backwards compatible!)

0.2.0 (2015-09-09)
------------------

* Updated library to be compatible with Kong 0.5.x (WARNING: Not backwards compatible!)

0.1.14 (2015-08-26)
-------------------

* Added some error checks

0.1.13 (2015-08-26)
-------------------

* Small bugfix

0.1.12 (2015-08-20)
-------------------

* Implemented retrieve api for APIPluginConfigurationAdminContract

0.1.11 (2015-08-19)
-------------------

* Implemented close method for KongAdminContract

0.1.10 (2015-08-18)
-------------------

* Implemented Basic Auth credentials API's
* Implemented Key authentication API's
* Implemented OAuth2 API's

0.1.9 (2015-08-06)
------------------

* Improved error handling in client

0.1.8 (2015-08-06)
------------------

* Bugfixes

0.1.7 (2015-07-30)
------------------

* Implemented APIAdminContract.add_or_update API
* Implemented APIPluginConfigurationAdminContract.create_or_update API
* Implemented ConsumerAdminContract.create_or_update API

0.1.6 (2015-07-28)
------------------

* Updated KongAdminSimulator constructor to accept api_url

0.1.5 (2015-07-28)
------------------

* Added CollectionMixin to contract (abstract base classes)

0.1.4 (2015-07-28)
------------------

* Bugfix related to checking for API conflicts

0.1.3 (2015-07-28)
------------------

* Added more tests and 'CollectionMixin' that exposes an 'iterate' api

0.1.2 (2015-07-27)
------------------

* Implemented 'plugin configuration' update API

0.1.1 (2015-07-24)
------------------

* Package structure updated

0.1.0 (2015-07-23)
------------------

* First release on PyPI.



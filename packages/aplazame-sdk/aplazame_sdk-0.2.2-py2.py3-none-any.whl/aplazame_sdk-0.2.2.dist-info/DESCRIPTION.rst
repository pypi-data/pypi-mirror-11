Aplazame Python Sdk
===================

|Build Status| |Wheel| |Drone| |Requirements Status| |Coveralls| |Code Climate|

|Aplazame|

`Aplazame`_, a consumer credit company, offers a payment system that can be
used by online buyers to receive funding for their purchases.

Installation
------------

To install aplazame-sdk, simply:

.. code:: sh

    $ pip install aplazame-sdk

Usage
-----

.. code:: python

    >>> import aplazame_sdk
    >>> client = aplazame_sdk.Client('token', sandbox=True, version='1', ctype='json')
    >>> r = client.orders(page=2)
    >>> r.json()
    {
      "cursor": {
        "after": 3,
        "before": 1
      },
      "paging": {
        "count": 314,
        "next": "https://api.aplazame.com/orders?page=3",
        "previous": "https://api.aplazame.com/orders?page=1"
      },
      "results": [
      ]
    }
    >>> r.status_code
    200

Http
----

.. code:: http

    GET /orders HTTP/1.1
    Accept: application/vnd.aplazame.sandbox.v1+json
    Authorization: Bearer ->token<-
    Host: api.aplazame.com

    HTTP/1.1 200 OK
    Content-Type: application/vnd.aplazame.sandbox.v1+json

Documentation
-------------

Documentation is available at `docs.aplazame.com`_.

.. _Aplazame: https://aplazame.com
.. _docs.aplazame.com: http://docs.aplazame.com


.. |Build Status| image:: https://img.shields.io/pypi/v/aplazame-sdk.svg
   :target: https://pypi.python.org/pypi/aplazame-sdk
.. |Wheel| image:: https://img.shields.io/pypi/wheel/aplazame-sdk.svg
   :target: https://pypi.python.org/pypi/aplazame-sdk
.. |Downloads| image:: https://img.shields.io/pypi/dm/aplazame-sdk.svg
   :target: https://pypi.python.org/pypi/aplazame-sdk
.. |Requirements Status| image:: https://requires.io/github/aplazame/aplazame-sdk/requirements.svg?branch=master
   :target: https://requires.io/github/aplazame/aplazame-sdk/requirements/?branch=master
.. |Drone| image:: http://drone.aplazame.com/api/badge/github.com/aplazame/aplazame-sdk/status.svg?branch=master
   :target: http://drone.aplazame.com/github.com/aplazame/aplazame-sdk
.. |Coveralls| image:: https://coveralls.io/repos/aplazame/aplazame-sdk/badge.svg?branch=HEAD&service=github
   :target: https://coveralls.io/github/aplazame/aplazame-sdk?branch=HEAD
.. |Code Climate| image:: https://codeclimate.com/github/aplazame/aplazame-sdk/badges/gpa.svg
   :target: https://codeclimate.com/github/aplazame/aplazame-sdk
.. |Aplazame| image:: https://aplazame.com/static/img/banners/banner-728-white-python.png
   :target: https://aplazame.com


Change Log
==========

`0.2.2`_ (2015-09-15)
---------------------

`Full Changelog v0.2.2`_

* Fix lists kwargs
* Add /me and operations
* ci pull request strategy
* ci publish on pypi
* ci package versioning

`0.2.1`_ (2015-08-24)
---------------------

`Full Changelog v0.2.1`_

* ci deploy master
* Simulator request
* Fix minor errors

`0.2.0`_ (2015-07-20)
---------------------

* Makefile
* ci with drone.io
* Coverage 100%
* Test and build requirements
* Add badges
* Get method params strategy

.. _0.2.0: https://github.com/aplazame/aplazame-sdk/tree/v0.2.0
.. _0.2.1: https://github.com/aplazame/aplazame-sdk/tree/v0.2.1
.. _0.2.2: https://github.com/aplazame/aplazame-sdk/tree/v0.2.2
.. _Full Changelog v0.2.1: https://github.com/aplazame/aplazame-sdk/compare/v0.2.0...v0.2.1
.. _Full Changelog v0.2.2: https://github.com/aplazame/aplazame-sdk/compare/v0.2.1...v0.2.2



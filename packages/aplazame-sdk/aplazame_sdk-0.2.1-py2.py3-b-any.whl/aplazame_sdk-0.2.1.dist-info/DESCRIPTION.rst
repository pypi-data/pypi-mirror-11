Aplazame Python Sdk
===================

|Build Status| |Wheel| |Downloads| |Drone| |Coveralls| |Code Climate|

|Aplazame|

Aplazame, a consumer credit company, offers a payment system that can be
used by online buyers to receive funding for their purchases.

Installation
------------

To install aplazame-sdk, simply:

.. code:: sh

    $ pip install aplazame-sdk

Usage
-----

.. code:: python

    >>> from aplazame_sdk import Client
    >>> client = Client('->AccessToken<-', sandbox=True, version='1', ctype='json')
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
    Authorization: Bearer ->AccessToken<-
    Host: api.aplazame.com

    HTTP/1.1 200 OK
    Content-Type: application/vnd.aplazame.sandbox.v1+json

Documentation
-------------

Documentation is available at `docs.aplazame.com`_.

.. _docs.aplazame.com: http://docs.aplazame.com


.. |Build Status| image:: https://img.shields.io/pypi/v/aplazame-sdk.svg
   :target: https://pypi.python.org/pypi/aplazame-sdk
.. |Wheel| image:: https://img.shields.io/pypi/wheel/aplazame-sdk.svg
   :target: https://pypi.python.org/pypi/aplazame-sdk
.. |Downloads| image:: https://img.shields.io/pypi/dm/aplazame-sdk.svg
   :target: https://pypi.python.org/pypi/aplazame-sdk
.. |Drone| image:: http://drone.aplazame.com/api/badge/github.com/aplazame/aplazame-sdk/status.svg?branch=master
   :target: http://drone.aplazame.com/github.com/aplazame/aplazame-sdk
.. |Coveralls| image:: https://coveralls.io/repos/aplazame/aplazame-sdk/badge.svg?branch=HEAD&service=github
   :target: https://coveralls.io/github/aplazame/aplazame-sdk?branch=HEAD
.. |Code Climate| image:: https://codeclimate.com/github/aplazame/aplazame-sdk/badges/gpa.svg
   :target: https://codeclimate.com/github/aplazame/aplazame-sdk
.. |Aplazame| image:: https://aplazame.com/static/img/banners/banner-728-white.png
   :target: https://aplazame.com


Change Log
==========


`0.2.1`_ (2015-08-24)
-------------------

`Full Changelog`_

* Continuous integration deploy master
* Simulator request
* Fix minor errors

`0.2.0`_ (2015-07-20)
---------------------

`Full Changelog`_

* Makefile
* Continuous integration with drone
* Coverage 100%
* Test and build requirements
* Add badges
* Get method params strategy

.. _0.2.0: https://github.com/aplazame/aplazame-sdk/tree/v0.2.0
.. _0.2.1: https://github.com/aplazame/aplazame-sdk/tree/v0.2.1
.. _Full Changelog: https://github.com/aplazame/aplazame-sdk/compare/0.2.0...0.2.1



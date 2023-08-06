===============================
Infoblox Client
===============================

.. image:: https://img.shields.io/travis/bondar-pavel/infoblox-client.svg
        :target: https://travis-ci.org/infobloxopen/infoblox-client

.. image:: https://img.shields.io/pypi/v/infoblox-client.svg
        :target: https://pypi.python.org/pypi/infoblox-client


Client for interacting with Infoblox NIOS over WAPI.

* Free software: Apache license
* Documentation: https://infoblox-client.readthedocs.org.

Installation
------------

Install infoblox-client using pip:

::

  pip install infoblox-client

Usage
-----

Retrieve list of network views from NIOS:

::

  from infoblox_client import connector

  opts = {'host': '192.168.1.10', 'username': 'admin', 'password': 'admin'}
  conn = connector.Connector(opts)
  # get all network_views
  network_views = conn.get_object('networkview')


For this request data is returned as list of dicts:

::

  [{u'_ref': u'networkview/ZG5zLm5ldHdvcmtfdmlldyQw:default/true',
    u'is_default': True,
    u'name': u'default'}]


Features
--------

* TODO




History
-------

0.0.3 (2015-09-15)
____________________
* Added dependencies to package.


0.0.2 (2015-09-11)
____________________
* Fixed using dashes in package directory names that prevented package import after install.


0.0.1 (2015-09-11)
---------------------
* Added connector to send wapi requests to NIOS, does not includes NIOS object model at this point.

* First release on PyPI.



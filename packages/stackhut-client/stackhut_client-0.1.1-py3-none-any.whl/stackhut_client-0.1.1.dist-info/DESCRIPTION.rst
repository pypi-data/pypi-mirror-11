=======================
StackHut Client Library
=======================

.. image:: https://img.shields.io/travis/stackhut/client-python.svg
        :target: https://travis-ci.org/stackhut/client-python

.. image:: https://img.shields.io/pypi/v/stackhut-client.svg
        :target: https://pypi.python.org/pypi/stackhut-client

StackHut client library to call dev, local, and hosted StackHut services dynamically and asynchronously from your Python code as if it were a local function.

* Homepage: https://www.stackhut.com
* Free software: Apache license
* Documentation: https://stackhut.readthedocs.org.


Description
-----------

There are 3 main objects in the library,

SHService
^^^^^^^^^

This is the main library you create per service to communicate with it. It takes several parameters on construction, where those in square brackets are optional,

.. code:: python

    import stackhut_client as client
    client.SHService(author, service_name, [service_version], [auth], [host])

* author - The author of the service
* service_name - The service name
* version - The specific verion of the service (is `latest` if left blank)
* auth - An `SHAuth` object used to authenticate requests for private services
* host - URL for the StackHut API server, can be set to point to local servers during development, is `https://api.stackhut.com` if left blank

To make a remote call, just call the interface and method name on the service object, e.g.,

.. code:: python

    result = service.Interface.method(params, ...)


SHAuth
^^^^^^

An optional object used to authenticate requests to a service,

.. code:: python

    client.SHAuth(user, [hash], [token])

* user - Username of a registered StackHut user
* hash - Hash of the user's password (you can find this in ~/.stackhut.cfg). Be careful not to use in public-facing code. 
* token - A valid API token created for the user

One of `hash` or `token` must be present in the `auth` object to authorise a request by the given user.

SHError
^^^^^^^

Returned in the event of a remote service error in the catch block of a rejected promise.

The object has 3 parameters,

* code - The RPC error code
* message - A string describing the error
* data - An optional object that may contain additional structured data for handling the error

Example
-------

Using the existing service called `demo-nodejs` by user `stackhut`, we create the main service object,

.. code:: python

    import stackhut_client as client
    service = client.SHService('stackhut', 'web-tools')

>From here we can call any functions on any interfaces exposed by the hosted `stackhut/demo-nodejs` service, as follows,

.. code:: python

    result = service.Default.renderWebpage("http://www.stackhut.com", 1024, 768)
    print("Page render at {}".format(result))


Notes
^^^^^

* Python 3+ only currently (built on 3.4), looking into python-future for 2.x compatibility.
* Calls are currently synchronous but we will switch to an async-based solution following the release of Python 3.5.




=======
Credits
=======

Development Leads
-----------------

* Mandeep Gill <mandeep@stackhut.com>
* Leo Anthias <leo@stackhut.com>

.. Contributors
.. ------------
.. 
.. None yet. Why not be the first?
.. 


SILPA Webservice APIs
=====================

.. warning::

 Althoght SILPA JSON RPC Api is fully functional and silpa-flask itself
 uses it, the the api for listing the available methods is not
 functional now. We have plans for a http based api in the near future.
 As of now all the python functions available in the silpa modules can
 be accessed through the JSON RPC interface.


Introduction
------------

Silpa provides a set of webservice APIs over json-rpc protocol. Silpa
services can be used from any programming language which has an RPC
implementation. The request and response formats of APIs are in
json. It is recommended to read the `json-rpc documentation
<http://json-rpc.org/>`_  if you are
not familiar with that.

This page explains the available usage and sample usage from python
application. Implementing this in other programming languages should
not be difficult and should be a matter of changing the programming
language syntax.

For using the APIs you need the jsonrpc library of python. You can get
this from here.

Concepts
--------

JSON-RPC wraps an object, allowing you to call methods on that object
and get the return values.  It also provides a way to get error
responses.  The specification goes into the details (though in a vague
sort of way).  Here's the basics:

All access goes through a ``POST`` to a single URL.

The ``POST`` contains a ``JSON`` body that looks like::

  {"method": "methodName",

  "id": "arbitrary-something",
  "params": [arg1, arg2, ...]}



The id parameter is just a convenience for the client to keep
track of which response goes with which request.  This makes
asynchronous calls (like an XMLHttpRequest) easier.  We just send
the exact same id back as we get, we never look at it.

The response is ``JSON``.  A successful response looks like::

  {"result": the_result,

  "error": null,
  "id": "arbitrary-something"}


The error response looks like::

  {"result": null,
  "error": {"name": "JSONRPCError",
  "code": (number 100-999),
  "message": "Some Error Occurred",
  "error": "whatever you want\n(a traceback?)"},
  "id": "arbitrary-something"}

It doesn't seem to indicate if an error response should have a 200
response or a 500 response.  So as not to be completely stupid about
HTTP, we choose a 500 resonse, as giving an error with a 200
response is irresponsible.

Usage
-----

just send a http ``POST`` request to the ``JSONRPC`` url
``dev.silpa.org.in/JSONRPC``::

 {"method": "moduelname.methodName",

  "id": "arbitrary-something",
  "params": [arg1, arg2, ...]}

you will recieve a JSON reply with required result.

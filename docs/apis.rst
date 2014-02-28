SILPA Webservice APIs
=====================

.. note::

   The old ``listMethods`` API call for JSONRPC is not yet implemented
   in new version see `issue #3
   <https://github.com/Project-SILPA/Silpa-Flask/issues/15>`_.


Introduction
------------

Silpa provides a set of webservice APIs over json-rpc protocol. Silpa
services can be used from any programming language which has an RPC
implementation. The request and response formats of APIs are in
json. It is recommended to read the `json-rpc documentation
<http://json-rpc.org/>`_ if you are not familiar with that.

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

All access goes through a ``POST`` to a single URL.The ``POST``
contains a ``JSON`` body that looks like

.. code-block:: json

   {
     "method": "methodName",
     "id": "arbitrary-something",
     "params": [arg1, arg2, ...],
   }


The id parameter is just a convenience for the client to keep track of
which response goes with which request.  This makes asynchronous calls
(like an XMLHttpRequest) easier.  We just send the exact same id back
as we get, we never look at it.

The response is ``JSON``.  A successful response looks like

.. code-block:: json

   {
     "result": the_result,
     "error": null,
     "id": "arbitrary-something",
   }


The error response looks like

.. code-block:: json

   {
     "result": null,
     "error": {"name": "JSONRPCError",
     "code": (number 100-999),
     "message": "Some Error Occurred",
     "error": "whatever you want\n(a traceback?)"},
     "id": "arbitrary-something",
   }

It doesn't seem to indicate if an error response should have a 200
response or a 500 response.  So as not to be completely stupid about
HTTP, we choose a 500 resonse, as giving an error with a 200
response is irresponsible.

Usage
-----

A sample usage using python can be seen below

.. code-block:: python

   from jsonrpclib import Server

   proxy = Server("http://silpa.org.in/JSONRPC")
   print proxy.scriptrender.render_text("Some text to render", "svg",
		100,200)

A sample usage using PHP can be seen below

.. code-block:: php

   define ('HOSTNAME', 'http://silpa.org.in/JSONRPC');
   $url = HOSTNAME;

   // Open the Curl session
   $session = curl_init($url);

   // If it's a POST, put the POST data in the body
		$postvars = '{"method": "scriptrender.render_text",
		"params": ["Your text goes here", "png", 100,100],
		"id":"jsonrpc"}';
   curl_setopt ($session, CURLOPT_POST, true);
   curl_setopt ($session, CURLOPT_POSTFIELDS, $postvars);

   // Don't return HTTP headers. Do return the contents of the call
   curl_setopt($session, CURLOPT_HEADER, false);
   curl_setopt($session, CURLOPT_RETURNTRANSFER, true);

   // Make the call
   $json = curl_exec($session);

   // The web service returns json. Set the Content-Type appropriately
   header("Content-Type: application/json");
   echo $json;
   $obj =  json_decode($json,false);
   $result  =  $obj->{"result"};
   echo $result;
   curl_close($session);

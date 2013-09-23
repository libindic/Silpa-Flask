Silpa-Flask
===========

Silpa-Flask is a webapp built using `flask <flask.pocoo.org/‎>`_ to
host the silpa modules and provide a web interface for them as well as
make them accessible through the JSONRPC interface.


Writing a module for Silpa-Flask
--------------------------------

All silpa modules are implemented as classes with member functions
which will be exposed through the JSONRPC interface. All the modules
are required to  implement a ``getInstance()`` method that will return
an instance of the corresponding class. If  you are also adding a
web interface then you are required to create a templates folder in
the root of your python package and create a jinja template with the
name ``<modulename>.html``. The template should also extend the
template  ``silpa.html``. If this is not clear then feel free to look
at the source of any of the modules.

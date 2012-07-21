SILPA
==========
SILPA - Indian Language computing platform which provides a web interface
for different Indian language computing python modules. This is hosted at
http://silpa.org.in

This is a new SILPA platform a.k.a restructuring is in progress. I'm trying to
use Flask microframe work and Jinja2 templating system. Additionally modules
are moved out of the original SILPA code thus providing a way for developer to
develop a python module without bothering about internals of SILPA itself.

How To Run?
==========
Note that this is currently a work in progress. So things may not work as you
expected it to work. If you want to test this you need to have following installed
on your system

* Flask
* Jinja2
* Werkzeug
* Virtualenv

If you don't want to spoil your system install following modules separated from original
source code in virtual environment created using VirtualEnv module

* [Soudex ](http://github.com/copyninja/Soundex)
* [ApproxSearch](http://github.com/copyninja/ApproxSearch)
* [Transliteration](http://github.com/copyninja/Transliteration)

Currently only these 2 modules are used but you can include more you can find some more modules
in my Github account, install them and add a line in *silpa.conf* for enabling them.

Additionally we would need a *normalizer* module for *Transliteration* modules correct working.
Get it from below URL and install it in your virtual environment but ***Do not add a line to silpa.conf
for this module. Its not a web module pure python module*** 

Wanna Help?
==========

Your help is most welcome. You can do following to help me

1. Help me separate out modules from original Silpa
2. Use it and report me bugs
3. Help me update docs
4. Get a new design for SILPA


TODO
==========

1. Implement JSONRPC so these modules can actually function [Done]
2. Serve Documentation and other pages through Flask and implement Jinja2 
3. Get remaining modules of SILPA get their templates
4. Provide RESTful API for all modules

Known Bugs
===========

1. <p style="text-decoration: line-through;">Transliteration module is not in working state</p>
2. Hyphenate module breaks it needs guesslanguage module

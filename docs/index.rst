.. Silpa documentation master file, created by
   sphinx-quickstart on Fri Sep  6 18:28:20 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SILPA
-----

The project is named as Silpa, may be an acronym of Swathanthra(Mukth,
Free as in Freedom) Indian Language Processing Applications. It is a
web framework and a set of applications for processing Indian
Languages in many ways. Or in other words, it is a platform for
porting existing and upcoming language processing applications to the
web.

As it is meant for covering all languages of India, all modules should
be capable of handling all scripts from India(Sometimes English
too). At the same time , the language of input data is transparent ,
meaning, user need not mention that *this* is the language in which
she is entering the data. Unlike desktop applications which asks to
specify the language along with the input data(for eg: Spell checker)
, the modules should try to detect the language them self. And if
possible, modules try to process the data even if the input data is in
multiple Indic scripts.

The modules may be General purpose(eg: Dictionary,
Spellcheck,Sort. Transliteration, Font conversion..) or
Technology/Algorithm Demonstration purpose (eg: Hyphenation, Stemmer,
Search algorithms)

The modules work as standalone python packages which will serve their
purpose and also they plug into the silpa-flask webframewok so that
they can be accessed as web services also, or become just another
webapp like the dictionary module.

Some of the modules are usable as of now, while some of them are in
development. You may just try out them. User's data will not be logged
exceptwhen a crash occurs(at that time user data and exception trace
will be logged for later debugging).

Contents:

.. toctree::
   :maxdepth: 2

   installation
   silpa-flask
   listofmodules
   apis
   faq
   credits


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

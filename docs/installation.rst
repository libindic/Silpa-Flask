Install Instructions
========================

Note that this is currently a work in progress. So things may not work
as you expected it to work. If you want to test this you need to have
following installed on your system

* pip
* Virtualenv

Test deployment


Installing VirtualEnv
--------------------------

If you are on Mac OS X or Linux, chances are that one of the following
two commands will work for you:

.. code-block:: shell-session

   $ sudo easy_install virtualenv

or even better:

.. code-block:: shell-session

   $ sudo pip install virtualenv

One of these will probably install virtualenv on your system. Maybe
it’s even in your package manager. If you use Ubuntu, try:

.. code-block:: shell-session

   $ sudo apt-get install python-virtualenv

Once you have virtualenv installed, just fire up a shell-session and
create your own environment.

.. code-block:: shell-session

 $ virtualenv silpa

 New python executable in silpa/bin/python
 Installing distribute............done.


.. note:: You may want to use ``--system-site-packages`` option while
	  creating virtualenv as some of dependencies like ``pango``
	  and ``cairo`` will not install cleanly from ``pip``.

Now, whenever you want to work on a project, you only have to activate
the corresponding environment. On OS X and Linux, do the following:

.. code-block:: shell-session

 $ . silpa/bin/activate

If you are a Windows user, the following command is for you:

.. code-block:: shell-session

 $ silpa\scripts\activate.bat

Either way, you should now be using your virtualenv (notice how the
prompt of your shell-session has changed to show the active
environment).

Get the Code
---------------

.. code-block:: shell-session

    $ git clone https://github.com/Project-SILPA/Silpa-Flask.git
    $ cd Silpa-Flask
    $ pip install -r requirements.txt
    $ python silpa.py

If you want to Install all modules:

.. code-block:: shell-session

		$ pip install -r requirements-modules.txt

.. note:: Previously we were suggesting use of ``modules.txt`` but now
	  we are unable  properly update the pypi modules in time so
	  we suggest use of ``head`` of git repo. But note that this
	  might lead to some breakage.

To enable module a line should be added to *silpa.conf*. By default
all modules will be enabled if you don't want this behavior mark
``no`` infront of module name under ``modules``
section. ``modules_display`` section is used to display a text in the
side bar of SILPA main page. Tweak it if required.

.. warning::

 *normalizer* and *silpa_common* modules are helper modules which is
 required by the current modules.  Do not add a line to silpa.conf for
 this module. Its not a web module pure python module

Now you can just enter the following command to get Flask activated in
your virtualenv:

.. code-block:: shell-session

 $ pip install Flask

A few seconds later and you are good to go.

You can start the silpa application by

.. code-block:: shell-session

 python silpa.py
 Running on http://127.0.0.1:5000/


Hosting the SILPA on Webserver
-------------------------------------

SILPA can also be hosted on webserver like ``apache`` or
``nginx``. Here we utilize the ``uwsgi`` containers to contain our
application. It is also possible to use other methods which are
commonly used to host *WSGI* application. But here we give example of
*uWSGI* for hosting which we use on our servers.

For installing *uWSGI* on Debian based derivatives use following
command.

.. code-block:: shell-session

   $ sudo aptitude install uwsgi uwsgi-plugin-python

Now we need to create separate user for running silpa, its not
recommended to run uWSGI as root. For creating a user for SILPA run
following command

.. code-block:: shell-session

   $ sudo adduser --disabled-login --disabled-password silpa

.. note:: You can use different user name. Above is just an example
	  for creating new uid.

Once installed and uid is created you need to place following
configuration file under ``/etc/uwsgi/appas-available/silpa.ini``

.. code-block:: ini

   [uwsgi]
   single-interpreter = True
   plugins = 0:python
   chmod = 766

   uid = silpa
   wsgi-file = /path/to/silpa-flask/dispatch.wsgi
   virtualenv = /path/to/virtuanenv/created

   docroot = /path/to/silpa-flask

   touch-reload = %(docroot)/dispatch.wsgi
   touch-reload = %(docroot)/silpa.py
   touch-reload = %(docroot)/webbridge.py
   touch-reload = %(docroot)/loadconfig.py
   touch-reload = %(docroot)/silpa.conf

   callable = application
   backtrace-depth = 4

   master = True
   workers = 4
   cheaper = 2
   threads = 2

Now we need to enable this configuration for doing this we need to
symlink above file to ``/etc/uwsgi/apps-enabled``. Run following
commands to do this.

.. code-block:: shell-session

   cd /etc/uwsgi/apps-enabled/
   sudo ln -s ../uwsgi/apps-available/silpa.ini

Now to start the application container for SILPA run following comand.

.. code-block:: shell-session

   sudo service uwsgi start silpa

Now you can use apache2 or nginx as front end for your uWSGI
container. A example apache2 conf which we use is below.

.. code-block:: apacheconf

	NameVirtualHost *:80

	<VirtualHost *:80>
	    ServerName dev.silpa.org.in
	    ServerAlias www.dev.silpa.org.in
	    ServerAlias silpa.org.in
	    ServerAlias dev.silpa.org.in
	    ServerAdmin silpa-discuss@nongnu.org

	    DocumentRoot /path/to/silpa-flask

	    <Location />
	 	SetHandler uwsgi-handler
	 	uWSGISocket /var/run/uwsgi/app/silpa/socket
	 	uWSGImaxVars 512
	    </Location>


	    ErrorLog ${APACHE_LOG_DIR}/dev.silpa.org.in/error.log
	    LogLevel warn
	    CustomLog ${APACHE_LOG_DIR}/dev.silpa.org.in/access.log combined
	</VirtualHost>

.. note:: All above hosting documentation is suited for Debian
	  derivatives. If you are using some other distribution you
	  might need to tweak it suit your distribution files.

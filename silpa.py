from flask import Flask
from logging import handlers, Formatter
from webbridge import WebBridge
from core.modulehelper import enabled_modules, BASEURL, modules
from jinja2 import PackageLoader, ChoiceLoader
import loadconfig
import logging
import os


def register_url():
    '''
     Function all form of URL which will be handled by SILPA service

     This function actually make this flask front end of SILPA independent
     of any modules. It doesn't know what modules are present nor doesn't
     know how to handle modules all the request will be promptly handed over
     to WebBridge
    '''
    # / or /baseurl for index page
    baseurl = '/' if BASEURL == '/' else BASEURL
    app.logger.debug("Registering the URL:{0}".format(baseurl))
    app.add_url_rule(baseurl, view_func=WebBridge.as_view(baseurl))

    # Register all enabled modules
    # baseurl/modulenames['module']
    for module in enabled_modules:
        module_url = baseurl + "/" + module if not baseurl == "/" \
                else baseurl + module
        app.logger.debug("Registering the URL:{0}".format(module_url))
        app.add_url_rule(module_url, view_func=WebBridge.as_view(module_url))

    # JSONRPC url
    jsonrpc_url = (baseurl +
                    "/JSONRPC" if not baseurl == "/" else baseurl + "JSONRPC")
    app.logger.debug("Registering the URL:{0}".format(baseurl))
    app.add_url_rule(jsonrpc_url, view_func=WebBridge.as_view(jsonrpc_url))


def add_templates():
    templates = [app.jinja_loader]
    for key in modules.keys():
        if modules.get(key) == 'yes':
            templates.append(PackageLoader(key))
    app.jinja_loader = ChoiceLoader(templates)


def configure_logging():
    '''
      This function configures logging for the SILPA applications using Flask's
      internal logger.

      For now log file will be rotated 7 days once and 4 backups will be kept.
      This can't be modified using configuration file as of now.

      Default logging level will be ERROR and can be modified from
      configuration file. Log folder and file name can also be configured using
      configuration file but make sure the path  you give is writable for
      Webserver user, otherwise this will lead to an error.
    '''
    log_level = loadconfig.get('log_level')
    log_folder = loadconfig.get('log_folder')
    log_name = loadconfig.get('log_name')
    filename = os.path.join(log_folder, log_name)

    handler = handlers.TimedRotatingFileHandler(filename, when='D',
                                                interval=7, backupCount=4)

    level = logging.ERROR

    if log_level == "debug":
        level = logging.DEBUG
    elif log_level == "info":
        level = logging.INFO
    elif log_level == "warn":
        level = logging.WARNING
    elif log_level == "error":
        level = logging.ERROR

    handler.setLevel(level)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s \
                                   [in %(pathname)s %(lineno)d]'))

    app.logger.setLevel(level)
    app.logger.addHandler(handler)


DEBUG = False

# Basics
app = Flask(__name__)
app.config.from_object(__name__)

# Logging
configure_logging()

# Register URL's
register_url()

# adds templates from imported modules
add_templates()

if __name__ == '__main__':
    app.run()

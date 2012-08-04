from flask import Flask
from logging import handlers,Formatter
from webbridge import WebBridge
from core.modulehelper import enabled_modules, BASEURL
from core import modulehelper

import loadconfig
import logging


def register_url():
    '''
     Function all form of URL which will be handled by SILPA service

     This function actually make this flask front end of SILPA independent
     of any modules. It doesn't know what modules are present nor doesn't
     know how to handle modules all the request will be promptly handed over
     to WebBridge
    '''
    # / or /baseurl for index page
    baseurl = '/'  if BASEURL == '/' else '/' + BASEURL
    app.logger.debug("Registering the URL:{0}".format(baseurl))
    app.add_url_rule(baseurl, view_func=WebBridge.as_view(baseurl))

    # Register all enabled modules
    # baseurl/modulenames['module']
    for module in enabled_modules:
        module_url = baseurl + "/" + module if not baseurl == "/" else baseurl + module
        app.logger.debug("Registering the URL:{0}".format(baseurl))        
        app.add_url_rule(module_url, view_func=WebBridge.as_view(module_url))

    # JSONRPC url
    jsonrpc_url = baseurl + "/JSONRPC" if not baseurl == "/" else baseurl + "JSONRPC"
    app.logger.debug("Registering the URL:{0}".format(baseurl))    
    app.add_url_rule(jsonrpc_url,view_func=WebBridge.as_view(jsonrpc_url))

def configure_logging():
    log_level = loadconfig.get('log_level')
    log_folder = loadconfig.get('log_folder')
    log_name = loadconfig.get('log_name')
    filename = log_folder + '/' + log_name

    handler = handlers.TimedRotatingFileHandler(filename,when='D',interval=7,backupCount=4,encoding='utf-8')

    level = logging.ERROR
    if log_level == 'debug':
        level = logging.DEBUG
    elif log_level == "info":
        level = logging.INFO
    elif log_level == "warn":
        level = logging.WARNING
    elif log_level == "error":
        level = logging.ERROR

    handler.setLevel(level)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'
                                   '[in %(pathname)s:%(lineno)d]'))

    return handler

DEBUG = False

# Basics
app = Flask(__name__)
app.config.from_object(__name__)

# Logging
app.logger.addHandler(configure_logging())

# Register URL's
register_url()    

if __name__ == '__main__':
    app.run()

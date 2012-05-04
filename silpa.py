from flask import Flask
from webbridge import WebBridge
from core.modulehelper import enabled_modules, BASEURL
from core import modulehelper



app = Flask(__name__)
app.config.from_object(modulehelper.__name__)

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
    app.add_url_rule(baseurl, view_func=WebBridge.as_view(baseurl))

    # Register all enabled modules
    # baseurl/modulenames['module']
    for module in enabled_modules:
        module_url = baseurl + "/" + module if not baseurl == "/" else baseurl + module
        print module_url
        app.add_url_rule(module_url, view_func=WebBridge.as_view(module_url))

    # JSONRPC url
    jsonrpc_url = baseurl + "/JSONRPC" if not baseurl == "/" else baseurl + "JSONRPC"
    app.add_url_rule(jsonrpc_url,view_func=WebBridge.as_view(jsonrpc_url))
    


if __name__ == '__main__':
    # app.debug = True
    # Lets register all required URL's
    register_url()
    app.run()

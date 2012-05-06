'''
  WebBridge is a bridging class between the flask front end of SILPA with
  the module related information like rendering appropriate templates and
  answering the JSONRPC requests and RESTful requests.

  This class is derived from MethodView class from flask.views
'''

from flask.views import MethodView
from flask import render_template, request
from core.modulehelper import modulenames, enabled_modules, BASEURL
from core.jsonrpchandler import JSONRPCHandler

handler = JSONRPCHandler()

class WebBridge(MethodView):

    def get(self):
        '''
         Method from MethodView class which handles all HTTP GET requests
         depending on request path render required template.

         If the query string is not None then its a RESTful request respond with
         a proper response format
        '''
        if request.path == "/":
            # request is for document root
            return render_template('index.html',title="SILPA",main_page=BASEURL, modules=enabled_modules)
        elif len(request.args) == 0:
            # This is not query so lets serve the page
            pathcomponent = request.path.split('/')[-1]
            if pathcomponent == modulenames['soundex']:
                return render_template('soundex.html',title="Soundex", main_page=BASEURL, modules=enabled_modules)
            elif pathcomponent == modulenames['inexactsearch']:
                return render_template('approxsearch.html',title="ApproxSearch",main_page=BASEURL, modules=enabled_modules)
            elif pathcomponent == modulenames['transliteration']:
                return render_template('transliterate.html', title="Indic Translieteration", main_page=BASEURL, modules=enabled_modules)
            elif pathcomponent == modulenames['hyphenation']:
                return render_template('hyphenator.html', title="Hyphenate", main_page=BASEURL, modules=enabled_modules)


    def post(self):
        '''
         Method from MethodView class which handles all HTTP POST requests

         In our case only POST requests will be for JSONRPC. This is how all pages
         work so we are retaining this else RESTful will be more modern way of doing
         stuff than RPC
        '''
        if request.path.split('/')[-1] == "JSONRPC":
            if request.data != None:
                result = handler.handle_request(request.data)
                return result


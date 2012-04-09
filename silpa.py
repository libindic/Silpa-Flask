from flask import Flask, request, g, redirect, url_for,\
    abort, render_template, flash
import constants
from constants import modules,modulenames

app = Flask(__name__)
app.config.from_object(constants.__name__)


@app.route('/Soundex')
def Soundex():
    '''
      This function is responsible to handle the /Soundex module page request.
      It just returns the rendered template
    '''
    return render_template('soundex.html',title='Soundex Module',modules = (modulenames[x] for x  in modules.keys() if modules[x] == "yes"))

@app.route('/ApproxSearch')
def ApproxSearch():
    '''
      This function is responsible to handle the /ApproxSearch module page request.
      It just returns the rendered template
    '''
    return render_template('approxsearch.html',title='ApproxSearch Module',modules = (modulenames[x] for x  in modules.keys() if modules[x] == "yes"))

@app.route('/JSONRPC')
def JSONRPC():
    '''
     This module is responsible for handling module processing request which is implemented
     as JSONRPC.

     #TODO: Implement it :P
    '''
    pass

@app.route('/')
def main_page():
    '''
     This function renders the main page of Silpa
    '''
    return render_template('index.html',title='SILPA',modules=(modulenames[x] for x in modules.keys() if modules[x] == "yes"))


if __name__ == '__main__':
    app.debug = True
    # Lets intialized enabled module before starting server
    constants.load_modules()
    app.run()

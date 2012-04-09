from flask import Flask, request, g, redirect, url_for,\
    abort, render_template, flash

import sys
import constants
from constants import modules,modulenames,MODULES


def load_modules():
    '''
      Load the modules enabled in the configuration file
      by user. This function initializes global variable
      MODULES which is a dictionary having module name as
      key and module itself as value. Which can be used later
      to process requests coming for the modules.
    '''

    for key in modules.keys():
        if modules.get(key) == 'yes':
            mod = None
            try:
                mod = sys.modules[key]
                if not type(mod).__name__ == 'module':
                    raise KeyError
            except KeyError:
                mod = __import__(key,globals(),locals(),[])
                mod = getattr(mod,key)
                sys.modules[key] = mod.getInstance()
            if mod:
                MODULES[key] = mod.getInstance()


app = Flask(__name__)
app.config.from_object(constants.__name__)


@app.route('/Soundex')
def Soundex():
    return render_template('soundex.html',title='Soundex Module',modules = (modulenames[x] for x  in modules.keys() if modules[x] == "yes"))

@app.route('/ApproxSearch')
def ApproxSearch():
    return render_template('approxsearch.html',title='ApproxSearch Module',modules = (modulenames[x] for x  in modules.keys() if modules[x] == "yes"))

@app.route('/JSONRPC')
def JSONRPC():
    pass

@app.route('/')
def main_page():
    return render_template('index.html',title='Indic Computing Platform',modules=(modulenames[x] for x in modules.keys() if modules[x] == "yes"))

if __name__ == '__main__':
    app.debug = True
    app.run()

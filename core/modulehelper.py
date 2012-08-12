'''
  Purpose of this file is to hold variables which is used
  across the application so that these variables don't get initialized multiple times
'''

_all_ = ['MODULES', 'modules', 'modulenames', 'enabled_modules', 'load_modules', 'BASEURL']

import loadconfig
import sys


MODULES = {}
BASEURL = loadconfig.get('baseurl')

modules = loadconfig.get('modules')
modulenames = loadconfig.get('modules_display')

enabled_modules = [modulenames[x] for x in modules.keys() if modules[x] == "yes"]

def load_modules():
    '''
      Load the modules enabled in the configuration file
      by user. This function initializes global variable
      MODULES which is a dictionary having module name as
      key and module itself as value. Which can be used later
      to process requests coming for the modules.
    '''

    # Already initialized the modules then don't do it again
    if len(MODULES) != 0:
        return
    
    for key in modules.keys():
        if modules.get(key) == 'yes':
            mod = None
            try:
                mod = sys.modules[key]
                if not type(mod).__name__ == 'module':
                    raise KeyError
            except KeyError:
                try:
                    mod = __import__(key,globals(),locals(),[])
                    sys.modules[key] = mod
                except ImportError:
                    # Since we can't use logger from flask as its not yet
                    # activated we will write it to sys.stderr this should
                    # go to webserver error.log
                    print >> sys.stderr, "Failed to import module {0}".format(key)
                    pass
            if mod:
                MODULES[key] = mod.getInstance()

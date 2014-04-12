'''
  Purpose of this file is to hold variables which is used
  across the application so that these variables don't get
  initialized multiple times
'''

from loadconfig import config
from flask import globals

import importlib

_modules = [module for module, need in config.items("modules")
            if need == "yes"]


def load_modules():
    app = globals.current_app
    for module in _modules:
        try:
            importlib.import_module(module)
        except ImportError:
            app.logger.error("Failed to import {module}".format(module=module))

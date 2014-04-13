from __future__ import print_function
from loadconfig import config

import importlib
import sys

_modules = [module for module, need in config.items("modules")
            if need == "yes"]


def load_modules():
    for module in _modules:
        try:
            importlib.import_module(module)
        except ImportError:
            print("Failed to import {module}".format(module=module),
                  file=sys.stderr)

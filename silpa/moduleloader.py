from loadconfig import config
from flask import current_app

import importlib

_modules = [module for module, need in config.items("modules")
            if need == "yes"]


def load_modules():
    for module in _modules:
        try:
            importlib.import_module(module)
        except ImportError:
            current_app.logger.error(
                "Failed to import {module}".format(module=module))

from __future__ import print_function

import importlib
import sys


class ModuleConfigHelper(object):
    module_names = []
    module_display = {}
    base_url = None

    def __new__(cls, *args, **kwargs):
        config = kwargs['config']
        cls.module_names = {module for module, need in config.items('modules')
                            if need == 'yes'}

        cls.module_display = {module: display_name for module, display_name in
                              config.items('module_display')
                              if module in cls.module_names}
        cls.base_url = config.get('main', 'baseurl')
        return super(ModuleConfigHelper, cls).__new__(cls)

    @classmethod
    def get_modules(cls):
        return cls.module_names

    @classmethod
    def get_module_displaynames(cls):
        return cls.module_display

    @classmethod
    def get_baseurl(cls):
        return cls.base_url

    @classmethod
    def load_modules(cls):
        for module in cls.module_names:
            try:
                importlib.import_module(module)
            except ImportError as e:
                print("Failed to import {module}: {message}".
                      format(module=module, message=e.message),
                      file=sys.stderr)

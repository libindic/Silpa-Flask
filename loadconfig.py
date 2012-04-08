from ConfigParser import RawConfigParser
import os

_all_ = ['get']

class _SilpaConfig:
    def __init__(self):
        _config = RawConfigParser()
        _config.read('silpa.conf')

        self.site_name = _config.get('main','site')

        folder = _config.get('logging','log_folder')
        self.log_folder = folder if folder else os.getcwd()

        name = _config.get('logging','log_name')
        self.log_name = name if name else 'silpa.log'

        self.modules = {}
        for module,status in _config.items('modules'):
            self.modules[module] = status if status else "no"

        self.modules_display = {}
        for module,name in _config.items('module_display'):
            self.modules_display[module] = name

_config = _SilpaConfig()

def get(key):
    return _config.__dict__[key]
        
        

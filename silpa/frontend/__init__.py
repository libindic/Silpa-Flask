from .. import factory
from jinja2 import PackageLoader, ChoiceLoader
from ..loadconfig import config


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__,
                             settings_override)
    load_module_templates(app)
    return app


def load_module_templates(app):
    modules = [module for module, need in config.items('modules')
               if need == 'yes']
    templates = [app.jinja_loader]
    for module in modules:
        templates.append(PackageLoader(module))
    app.jinja_loader = ChoiceLoader(templates)

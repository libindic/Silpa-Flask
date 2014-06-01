from .. import factory
from jinja2 import PackageLoader, ChoiceLoader
from ..helper import ModuleConfigHelper


def create_app(conffile, settings_override=None):
    app = factory.create_app(__name__, __path__,
                             settings_override, conffile)
    load_module_templates(app)
    return app


def load_module_templates(app):
    modules = ModuleConfigHelper.get_modules()
    templates = [app.jinja_loader]
    for module in modules:
        templates.append(PackageLoader(module))
    app.jinja_loader = ChoiceLoader(templates)

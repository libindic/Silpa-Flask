from .. import factory
from functools import wraps
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


def route(bp, *args, **kwargs):
    def decorator(f):
        # FIXME: when we drop python2 support use unpack feature from
        # python3
        baseurl, module_display = args[0], args[1]
        for module in module_display:
            bp.add_url_rule(baseurl + module, view_func=f)

        @wraps(f)
        def wrapper(*args, **kwargs):
            print(args)
            print(kwargs)
            return f(*args, **kwargs)
        return f
    return decorator

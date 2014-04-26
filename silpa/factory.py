import pkgutil
import importlib
import logging
import os

from flask import Flask, Blueprint
from .loadconfig import config
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler


def register_blueprints(app, package_name, package_path):
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('{package}.{module}'.format(
            package=package_name, module=name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
                rv.append(item)
    return rv


def configure_logging(app):
    log_level = config.get('logging', 'log_level')
    log_folder = config.get('logging', 'log_folder')
    log_name = config.get('logging', 'log_name')

    handler = TimedRotatingFileHandler(os.path.join(log_folder, log_name),
                                       when='D', interval=7, backupCount=4)

    level = None

    if log_level == 'debug':
        level = logging.DEBUG
    elif log_level == 'info':
        level = logging.INFO
    elif log_level == 'error':
        level = logging.ERROR
    elif log_level == 'warn':
        level = logging.WARNING

    handler.setLevel(level)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s' +
                                   ' %(message)7s - [in %(funcName)s' +
                                   ' at %(pathname)s %(lineno)d]'))
    app.logger.setLevel(level)
    app.logger.addHandler(handler)


def create_app(package_name, package_path, settings_override=None):
    app = Flask(package_name, instance_relative_config=True)
    app.config.from_object("silpa.settings")
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    register_blueprints(app, package_name, package_path)
    configure_logging(app)

    return app

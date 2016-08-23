from flask import jsonify
from silpa import factory

def create_app(conffile, settings_override=None):
    app = factory.create_app(__name__, __path__,
                             settings_override, conffile)
    #app.errorhandler(404)(on_404)
    return app

from flask import jsonify
from functools import wraps
from .. import factory

import os


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            sc = 200 if 'error' not in result else 400
            return jsonify(result), sc
        return f
    return decorator


def create_app(settings_override=None):
    app = factory.create_app(__name__, os.path.dirname(__file__),
                             settings_override)
    app.errorhandler(404)(on_404)


def on_404(e):
    return jsonify(dict(error='Not Found')), 404

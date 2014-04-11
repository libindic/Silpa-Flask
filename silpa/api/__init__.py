from flask import jsonify
from functools import wraps


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            result = f(*args, **kwargs)
            return jsonify(result), sc
        return f
    return decorator

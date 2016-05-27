# -*- coding: utf-8 -*-
"""
    silpa.frontend.assets
    ~~~~~~~~~~~~~~~~~~~~~

    frontend application asset "pipeline"
"""

from flask.ext.assets import Environment, Bundle


css_all = Bundle("css/bootstrap.min.css",
                 "js/jquery.ime/css/jquery.ime.css",
                 "css/main.css", filters="cssmin", output="css/silpa.min.css")


js_all = Bundle("js/jquery.js",
                "js/bootstrap.min.js",
                "js/jquery.ime/src/jquery.ime.js",
                "js/jquery.ime/src/jquery.ime.inputmethods.js",
                "js/jquery.ime/src/jquery.ime.selector.js",
                "js/jquery.ime/src/jquery.ime.preferences.js",
                filters="jsmin", output="js/silpa.min.js")


def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    webassets.register('js_all', js_all)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug

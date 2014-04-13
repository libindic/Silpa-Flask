from flask import current_app, request, Blueprint, render_template, abort
from ..loadconfig import config
from . import route

_BASE_URL = config.get('main', 'baseurl')
_modules = [module for module, need in config.items('modules')
            if need == 'yes']
_modulename_to_display = sorted((display_name
                                 for module, display_name in
                                 config.items('module_display')
                                 if module in _modules))
_display_module_map = {display_name: module for module, display_name in
                       config.items('module_display')
                       if module in _modules}

bp = Blueprint('frontend', __name__)


@bp.route(_BASE_URL)
@bp.route(_BASE_URL + 'index.html')
@bp.route(_BASE_URL + 'License')
@bp.route(_BASE_URL + 'Credits')
@bp.route(_BASE_URL + 'Contact')
def serve_pages():
    if request.path == _BASE_URL:
        return render_template('index.html', title='SILPA',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)
    elif request.path == _BASE_URL + "License":
        return render_template('license.html', title='SILPA License',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)
    elif request.path == _BASE_URL + "Credits":
        return render_template('credits.html', title='Credits',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)
    elif request.path == _BASE_URL + "Contact":
        return render_template('contact.html', title='Contact SILPA Team',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)


@route(bp, _BASE_URL, _modulename_to_display)
def serve_module_page():
    request_mod = request.path.split('/')[-1]
    if request_mod in _display_module_map:
        return render_template(_display_module_map[request_mod] + '.html',
                               title=request_mod, main_page=_BASE_URL,
                               modules=_modulename_to_display)
    else:
        # Did we encounter something which is not registered by us?
        return abort(404)

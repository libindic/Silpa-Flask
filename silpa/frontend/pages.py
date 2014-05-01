from flask import Blueprint, render_template, abort
from ..loadconfig import config

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


@bp.route(_BASE_URL, defaults={'page': 'index.html'})
@bp.route(_BASE_URL + '<page>')
def serve_pages(page):
    if page == "index.html":
        return render_template('index.html', title='SILPA',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)
    elif page == "License":
        return render_template('license.html', title='SILPA License',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)
    elif page == "Credits":
        return render_template('credits.html', title='Credits',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)
    elif page == "Contact":
        return render_template('contact.html', title='Contact SILPA Team',
                               main_page=_BASE_URL,
                               modules=_modulename_to_display)
    else:
        # modules requested!.
        if page in _display_module_map:
            return render_template(_display_module_map[page] + '.html',
                                   title=page, main_page=_BASE_URL,
                                   modules=_modulename_to_display)
        else:
            # Did we encounter something which is not registered by us?
            return abort(404)

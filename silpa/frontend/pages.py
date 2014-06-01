from flask import Blueprint, render_template, abort
from ..helper import ModuleConfigHelper

_BASE_URL = ModuleConfigHelper.get_baseurl()
_modules = ModuleConfigHelper.get_modules()
_modulename_to_display = ModuleConfigHelper.get_module_displaynames()

_display_module_map = sorted(zip(_modulename_to_display.keys(),
                                 _modulename_to_display.values()))

bp = Blueprint('frontend', __name__)


@bp.route(_BASE_URL, defaults={'page': 'index.html'})
@bp.route(_BASE_URL + '<page>')
def serve_pages(page):
    if page == "index.html":
        return render_template('index.html', title='SILPA',
                               main_page=_BASE_URL,
                               modules=_display_module_map)
    elif page == "License":
        return render_template('license.html', title='SILPA License',
                               main_page=_BASE_URL,
                               modules=_display_module_map)
    elif page == "Credits":
        return render_template('credits.html', title='Credits',
                               main_page=_BASE_URL,
                               modules=_display_module_map)
    elif page == "Contact":
        return render_template('contact.html', title='Contact SILPA Team',
                               main_page=_BASE_URL,
                               modules=_display_module_map)
    else:
        # modules requested!.
        if page in _modules:
            return render_template(page + '.html',
                                   title=page, main_page=_BASE_URL,
                                   modules=_display_module_map)
        else:
            # Did we encounter something which is not registered by us?
            return abort(404)

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from silpa import api, frontend

application = DispatcherMiddleware(frontend.create_app(),
                                   {'/api': api.create_app()})

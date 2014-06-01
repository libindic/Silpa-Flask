from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from silpa import api, frontend
import os

conffile = os.path.join(os.path.dirname(__file__), "etc", "silpa.conf")

application = DispatcherMiddleware(frontend.create_app(conffile),
                                   {'/api': api.create_app(conffile)})

if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, application,
               use_reloader=True, use_debugger=True)

#!/usr/bin/python
#-*- mode: python -*-

from flup.server.fcgi import WSGIServer
from silpa import app

if __name__ == "__main__":
    WSGIServer(app).run()

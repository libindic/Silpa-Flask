#!/usr/bin/python
#-*- mode: python -*-

from wsgiref.handlers import CGIHandler
from silpa import app

CGIHandler().run(app)

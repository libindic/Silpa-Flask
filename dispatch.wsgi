#-*- mode: python -*-
import sys
import os

# For virtualenv deployment
activate_this = "/home/vasudev/Documents/Silpa/modules/moduletest/bin/activate_this.py"
try:
    execfile(activate_this,dict(__file__=activate_this))
except IOError:
    pass
    
sys.path.insert(0,os.path.dirname(__file__))
from silpa import app as application

# -*- coding: utf-8 -*-
"""
    tests.frontend
    ~~~~~~~~~~~~~~

    frontend tests package
"""

from silpa.frontend import create_app
from .. import SILPAAppTestCase, settings
import os


class SILPAFrontEndTestCase(SILPAAppTestCase):

    def _create_app(self):
        self.conffile = os.path.join(os.path.dirname(__file__), '../resources',
                                     'silpa.conf')
        return create_app(self.conffile, settings)

    def setUp(self):
        super(SILPAFrontEndTestCase, self).setUp()

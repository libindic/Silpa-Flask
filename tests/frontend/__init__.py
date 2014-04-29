# -*- coding: utf-8 -*-
"""
    tests.frontend
    ~~~~~~~~~~~~~~

    frontend tests package
"""

from silpa.frontend import create_app
from .. import SILPAAppTestCase, settings


class SILPAFrontEndTestCase(SILPAAppTestCase):

    def _create_app(self):
        return create_app(settings)

    def setUp(self):
        super(SILPAFrontEndTestCase, self).setUp()

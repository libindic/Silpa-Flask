# -*- coding: utf-8 -*-
"""
    tests.frontend.mainpage_tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    main page frontend tests module
"""

from . import SILPAFrontEndTestCase


class MainPageTestCase(SILPAFrontEndTestCase):

    def test_indexpage(self):
        r = self.get('/')
        self.assertIn('<title> SILPA - Indic Language Computing Platform ' +
                      '</title>', self.assertOk(r).data)

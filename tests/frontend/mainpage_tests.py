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

    def test_pages(self):
        r = self.get('/License')
        self.assertIn('<h1>License</h1>', self.assertOk(r).data)

        r = self.get('/Contact')
        self.assertIn('<h1>Contacts</h1>', self.assertOk(r).data)

        r = self.get('/Credits')
        self.assertIn('<h1>Credits</h1>', self.assertOk(r).data)

    def test_moduleloaded(self):
        from silpa.helper import ModuleConfigHelper
        module_display = ModuleConfigHelper.get_module_displaynames()

        r = self.get('/')
        self.assertOk(r)

        for m, d in module_display.items():
            # FIXME: Returned by configparser is unicode string for
            # some reason breaks with assertIn not sure why :(
            self.assertIn(d.encode('utf-8'), r.data)

            # TODO: URL in modules needs to be fixed befor enabling
            # below tests, for now skip transliteration which is
            # enabled in test conf but url is not fixed
            # if m != 'transliteration' and m != 'soundex':
            #  r1 = self.get('/' + m)
            #  self.assertIn('<title> {} - Indic Language Computing Platform' +
            #                ' </title>'.format(m), self.assertOk(r1).data)

    def test_pagenotfound(self):
        r = self.get('/blablabla')
        self.assertStatusCode(r, 404)

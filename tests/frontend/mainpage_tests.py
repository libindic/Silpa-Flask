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
        from silpa.loadconfig import config
        modules = [module for module, need in config.items('modules')
                   if need == "yes"]
        module_display = sorted((display_name
                                 for module, display_name in
                                 config.items('module_display')
                                 if module in modules))
        r = self.get('/')
        self.assertOk(r)

        for m in module_display:
            # FIXME: Returned by configparser is unicode string for
            # some reason breaks with assertIn not sure why :(
            self.assertIn(m.encode('utf-8'), r.data)

            # TODO: URL in modules needs to be fixed befor enabling
            # below tests
            # r1 = self.get('/' + m)
            # self.assertIn('<title> {} - Indic Language Computing Platform ' +
            #               '</title>', self.assertOk(r1).data)

# -*- coding: utf-8 -*-
'''
   tests.test_config
   ~~~~~~~~~~~~~~~~~

   Test various configuration parsing
'''

import testscenarios
import os

from functools import partial
from silpa.loadconfig import IncompleteConfigError, Config

resource_path = partial(os.path.join, os.path.dirname(__file__), 'resources')


class TestConfigParser(testscenarios.TestWithScenarios):
    scenarios = [
        ('main:site Missing Conf',
         dict(location=resource_path('silpa_main_site.conf'),
              section='main', option='site')),
        ('main:baseurl Missing Conf',
         dict(location=resource_path('silpa_main_baseurl.conf'),
              section='main', option='baseurl')),
        ('logging:log_level Missing Conf',
         dict(location=resource_path('silpa_logging_loglevel.conf'),
              section='logging', option='log_level')),
        ('logging:log_folder Missing Conf',
         dict(location=resource_path('silpa_logging_logfolder.conf'),
              section='logging', option='log_folder')),
        ('logging:log_name Missing Conf',
         dict(location=resource_path('silpa_logging_logname.conf'),
              section='logging', option='log_name')),
        ('modules Missing Conf',
         dict(location=resource_path('silpa_modules.conf'),
              section='modules', option=None)),
        ('modules_display Missing Conf',
         dict(location=resource_path('silpa_module_display.conf'),
              section='module_display', option=None))
    ]

    def test_config_error_handling(self):
        with self.assertRaises(IncompleteConfigError) as ic:
            Config(self.location)

        e = ic.exception
        self.assertEqual(self.option, e.option)
        self.assertEqual(self.section, e.section)

        if self.option:
            error = e.__str__()
            self.assertIn(self.option, error)
            self.assertIn(self.section, error)
        else:
            self.assertIn(self.section, e.__str__())

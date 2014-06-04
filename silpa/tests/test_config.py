#-*- coding: utf-8 -*-
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
         dict(location=resource_path('silpa_main_site.conf'))),
        ('main:baseurl Missing Conf',
         dict(location=resource_path('silpa_main_baseurl.conf'))),
        ('logging:log_level Missing Conf',
         dict(location=resource_path('silpa_logging_loglevel.conf'))),
        ('logging:log_folder Missing Conf',
         dict(location=resource_path('silpa_logging_logfolder.conf'))),
        ('logging:log_name Missing Conf',
         dict(location=resource_path('silpa_logging_logname.conf'))),
        ('modules Missing Conf',
         dict(location=resource_path('silpa_modules.conf'))),
        ('modules_display Missing Conf',
         dict(location=resource_path('silpa_module_display.conf')))
    ]

    def setUp(self):
        # No other better way to test
        self.config = Config()

    def test_config_error_handling(self):
        self.assertRaises(IncompleteConfigError,
                          self.config.__init__(self.location))

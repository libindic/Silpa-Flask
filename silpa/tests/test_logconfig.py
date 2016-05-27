# -*- coding: utf-8 -*-
'''
    silpa.tests.test_logconfig
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test loglevel configuration code
'''

import testscenarios
import os
import logging

from functools import partial
from silpa.api import create_app

resource_path = partial(os.path.join, os.path.dirname(__file__),
                        'resources')


class TestLogLevelConfiguration(testscenarios.TestWithScenarios):
    scenarios = [
        ('Info level configuration',
         dict(location=resource_path('silpa_info.conf'),
              level=logging.INFO)),
        ('Error level configuration',
         dict(location=resource_path('silpa_error.conf'),
              level=logging.ERROR)),
        ('Warning level configuration',
         dict(location=resource_path('silpa_warn.conf'),
              level=logging.WARNING)),
    ]

    def test_logging_level(self):
        app = create_app(self.location)
        self.assertEqual(self.level, app.logger.level)

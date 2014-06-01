from silpa.api import create_app
from .. import SILPAAppTestCase, settings
import os


class SILPAApiTestCase(SILPAAppTestCase):

    def _create_app(self):
        self.conffile = os.path.join(os.path.dirname(__file__), '../resources',
                                     'silpa.conf')
        return create_app(self.conffile, settings)

    def setUp(self):
        super(SILPAApiTestCase, self).setUp()

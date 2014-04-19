from silpa.api import create_app
from .. import SILPAAppTestCase, settings


class SILPAApiTestCase(SILPAAppTestCase):

    def _create_app(self):
        return create_app(settings)

    def setUp(self):
        super(SILPAApiTestCase, self).setUp()

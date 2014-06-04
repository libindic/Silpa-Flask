
from unittest import TestCase
from .utils import SILPATestCaseMixin


class SILPATestCase(TestCase):
    pass


class SILPAAppTestCase(SILPATestCaseMixin, SILPATestCase):
    def _create_app(self):
        raise NotImplementedError

    def setUp(self):
        super(SILPAAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        super(SILPAAppTestCase, self).tearDown()
        self.app_context.pop()

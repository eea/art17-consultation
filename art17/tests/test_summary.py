from unittest import TestCase
from flask.ext.webtest import TestApp
from art17.app import create_app
from art17.models import db


class BaseTest(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = TestApp(self.app, db=db, use_session_scopes=True)


class SummaryTests(BaseTest):

    def test_filter_group_has_values(self):
        pass

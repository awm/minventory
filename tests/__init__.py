import platform

from flask.testing import FlaskClient
from flask.ext.testing import TestCase
# from flask.ext.fillin import FormWrapper

from app import app, db
from manage import sampledata

def version_base():
    version = platform.python_version_tuple()
    if int(version[0]) == 2 and int(version[1]) <= 6:
        return Python26AssertionMixin
    else:
        return TestCase

class Python26AssertionMixin(TestCase):
    def assertIsNone(self, x, msg=None):
        self.assertTrue(x is None, msg)
    
    def assertIsNotNone(self, x, msg=None):
        self.assertTrue(x is not None, msg)
    
    def assertIn(self, a, b, msg=None):
        self.assertTrue(a in b, msg)
    
    def assertNotIn(self, a, b, msg=None):
        self.assertFalse(a in b, msg)

# class FormFlaskClient(FlaskClient):
#     def __init__(self, *args, **kwargs):
#         kwargs['response_wrapper'] = FormWrapper
#         super(FormFlaskClient, self).__init__(*args, **kwargs)

class TestBase(version_base()):
    config = {
        'SQLALCHEMY_DATABASE_URI': "sqlite://",
        'TESTING': True,
        'DEBUG': True,
        'WTF_CSRF_ENABLED': False
    }

    def create_app(self):
        app.config.update(self.config)
        # app.test_client_class = FormFlaskClient
        return app
    
    def setUp(self):
        self.db = db
        sampledata(output=False)
    
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

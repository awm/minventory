import platform

from flask import json
from flask.testing import FlaskClient
from flask.ext.testing import TestCase

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

# This wrapper assumes that the data is specified in the kwargs and that the content type is not provided
class JsonFlaskClient(FlaskClient):
    def _do_thing(self, func, args, kwargs):
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        kwargs['content_type'] = "application/json"
        return func(*args, **kwargs)

    def get_json(self, *args, **kwargs):
        return self._do_thing(self.get, args, kwargs)
    def patch_json(self, *args, **kwargs):
        return self._do_thing(self.patch, args, kwargs)
    def post_json(self, *args, **kwargs):
        return self._do_thing(self.post, args, kwargs)
    def put_json(self, *args, **kwargs):
        return self._do_thing(self.put, args, kwargs)

class TestBase(version_base()):
    config = {
        'SQLALCHEMY_DATABASE_URI': "sqlite://",
        'TESTING': True,
        'DEBUG': True,
        'WTF_CSRF_ENABLED': False
    }

    def create_app(self):
        app.config.update(self.config)
        app.test_client_class = JsonFlaskClient
        return app
    
    def setUp(self):
        self.db = db
        sampledata(output=False)
    
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def assert204(self, response, message=None):
        self.assertStatus(response, 204, message)

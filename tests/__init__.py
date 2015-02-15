from flask.testing import FlaskClient
from flask.ext.testing import TestCase
# from flask.ext.fillin import FormWrapper

from app import app, db
from manage import sampledata

# class FormFlaskClient(FlaskClient):
#     def __init__(self, *args, **kwargs):
#         kwargs['response_wrapper'] = FormWrapper
#         super(FormFlaskClient, self).__init__(*args, **kwargs)

class TestBase(TestCase):
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

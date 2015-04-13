from tests import TestBase
from flask import session

class LoginTest(TestBase):
    def test_load(self):
        with self.client as c:
            r = c.get("/auth/login")
            self.assert405(r)
            self.assertNotIn('user_id', session)

    def test_login(self):
        with self.client as c:
            r = c.post_json("/auth/login", data={'username': "admin", 'password': "1234"})
            self.assert200(r)
            self.assertIn('user_id', session)

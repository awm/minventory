from tests import TestBase
from flask import session

class LoginTest(TestBase):
    uri = "/auth/login"

    def test_invalid_methods(self):
        """Invalid login methods and content types"""
        with self.client as c:
            r = c.get(self.uri)
            self.assert405(r)
            self.assertNotIn('user_id', session)
            r = c.post(self.uri, data={'username': "admin", 'password': "1234"})
            self.assert400(r)
            self.assertNotIn('user_id', session)
            r = c.put_json(self.uri, data={'username': "admin", 'password': "1234"})
            self.assert405(r)
            self.assertNotIn('user_id', session)
            r = c.put_json(self.uri, data={'username': "admin", 'password': "1234"})
            self.assert405(r)
            self.assertNotIn('user_id', session)
            r = c.patch_json(self.uri, data={'username': "admin", 'password': "1234"})
            self.assert405(r)
            self.assertNotIn('user_id', session)
            r = c.delete(self.uri)
            self.assert405(r)
            self.assertNotIn('user_id', session)
            r = c.head(self.uri)
            self.assert405(r)
            self.assertNotIn('user_id', session)

    def test_valid_methods(self):
        """Valid login methods other than POST"""
        with self.client as c:
            r = c.options(self.uri)
            self.assert200(r)
            self.assertNotIn('user_id', session)

    def test_login(self):
        """Valid login"""
        with self.client as c:
            r = c.post_json(self.uri, data={'username': "admin", 'password': "1234"})
            self.assert200(r)
            self.assertIn('user_id', session)

    def test_invalid(self):
        """Invalid logins"""
        with self.client as c:
            r = c.post_json(self.uri, data={'username': "admin1", 'password': "1234"})
            self.assert401(r)
            self.assertNotIn('user_id', session)
            r = c.post_json(self.uri, data={'username': "admin", 'password': "12345"})
            self.assert401(r)
            self.assertNotIn('user_id', session)

class LogoutTest(TestBase):
    uri = "/auth/logout"

    def test_invalid_methods(self):
        """Invalid logout methods"""
        with self.client as c:
            r = c.get(self.uri)
            self.assert405(r)
            r = c.put_json(self.uri)
            self.assert405(r)
            r = c.put_json(self.uri)
            self.assert405(r)
            r = c.patch_json(self.uri)
            self.assert405(r)
            r = c.delete(self.uri)
            self.assert405(r)
            r = c.head(self.uri)
            self.assert405(r)

    def test_valid_methods(self):
        """Valid logout methods"""
        with self.client as c:
            r = c.options(self.uri)
            self.assert200(r)
            r = c.post(self.uri)
            self.assert401(r)

    def test_logout(self):
        """Valid logout"""
        with self.client as c:
            r = c.post_json("/auth/login", data={'username': "admin", 'password': "1234"})
            self.assert200(r)
            self.assertIn('user_id', session)
            r = c.post(self.uri)
            self.assert204(r)
            self.assertNotIn('user_id', session)

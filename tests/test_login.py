from tests import TestBase
from flask import session

class LoginTest(TestBase):
    def test_load(self):
        with self.client as c:
            r = c.get("/auth/login")
            self.assert200(r)
            self.assertTemplateUsed("auth/login.html")
            self.assertNotIn('user_id', session)

    def test_login(self):
        # r = self.client.get("/auth/login")
        # r.form.fields['username'] = "admin"
        # r.form.fields['password'] = "1234"
        # r = r.form.submit()
        with self.client as c:
            r = c.post("/auth/login", data={'username': "admin", 'password': "1234"})
            self.assertRedirects(r, "/")
            self.assertIn('user_id', session)

import time
from front_end_tests import TestBase, login
from flask import url_for, session, g
from flaskr.db import get_db

class TestLogin(TestBase):

    def test_login(self):
        """
        Tests that a user can login w/ valid input and is redirected to home page
        """
        login(self, "test", "test")
        assert url_for('blog.index') in self.driver.current_url
        # TODO
        # assert session['user_id'] == 1
        # assert g.user['username'] == 'test'

    def test_login_with_no_username(self):
        """
        Tests that the form is not sent when the username is blank
        """
        login(self, "", "test")
        assert url_for('auth.login') in self.driver.current_url

    def test_login_with_no_password(self):
        """
        Tests that the form is not sent when the password is blank.
        """
        login(self, "test", "")
        assert url_for('auth.login') in self.driver.current_url

    def test_logout(self):
        """
        Tests that the session is cleared and the user is redirected home
        """
        login(self, "test", "test")
        assert url_for('blog.index') in self.driver.current_url

        self.driver.find_element_by_id("logout_link").click()
        assert 'user_id' not in session
        assert url_for('blog.index') in self.driver.current_url

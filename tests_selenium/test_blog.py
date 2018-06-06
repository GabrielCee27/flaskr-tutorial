import time
from front_end_tests import TestBase, login
from flask import url_for, session, g
from flaskr.db import get_db

class TestBlog(TestBase):

    def test_flaskr_btn(self):
        """
        Tests that the user is redirected to home page through flaskr button
        """
        self.driver.find_element_by_id("flaskr_btn").click()

        assert url_for('blog.index') in self.driver.current_url


    def test_index(self):
        """
        Tests that the user is presented with 'Login' & 'Register' options at
        home page when not signed in. Also tests that when the user is signed in
        the nav tab displays 'Log Out'
        """
        self.driver.find_element_by_id("flaskr_btn").click()
        assert self.driver.find_element_by_id("login_link")
        assert self.driver.find_element_by_id("register_link")

        login(self, "test", "test")
        self.driver.find_element_by_id("flaskr_btn").click()
        time.sleep(5)
        assert self.driver.find_element_by_id("logout_link")

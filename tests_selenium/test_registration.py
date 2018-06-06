import time
from front_end_tests import TestBase
from flask import url_for
from flaskr.db import get_db

class TestRegistration(TestBase):

    def test_registration(self):
        """
        Test that given valid input the user is redirected to the login page,
        and that the user was successfully placed into database.
        """
        self.driver.find_element_by_id("register_link").click()
        self.driver.find_element_by_id("username").send_keys("test_user_name2")
        self.driver.find_element_by_id("password").send_keys("test_user_password2")
        self.driver.find_element_by_id("submit_btn").click()

        assert url_for('auth.login') in self.driver.current_url
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test_user_name'",
        ).fetchone is not None

    def test_registration_with_no_username(self):
        """
        Tests that the form is not sent when the username is blank.
        """
        self.driver.find_element_by_id("register_link").click()
        self.driver.find_element_by_id("username").send_keys("")
        self.driver.find_element_by_id("password").send_keys("test_user_password")
        self.driver.find_element_by_id("submit_btn").click()

        assert url_for('auth.register') in self.driver.current_url

    def test_registration_with_no_password(self):
        """
        Tests that the form is not sent when the password is blank.
        """
        self.driver.find_element_by_id("register_link").click()
        self.driver.find_element_by_id("username").send_keys("test_user_name")
        self.driver.find_element_by_id("password").send_keys("")
        self.driver.find_element_by_id("submit_btn").click()

        assert url_for('auth.register') in self.driver.current_url

    def test_already_registered_user(self):
        """
        Tests that an error massage is shown and the user is not redirected
        """
        self.driver.find_element_by_id("register_link").click()
        self.driver.find_element_by_id("username").send_keys("test")
        self.driver.find_element_by_id("password").send_keys("test")
        self.driver.find_element_by_id("submit_btn").click()

        assert "already registered" in self.driver.find_element_by_id("error_flash_message").text
        assert url_for('auth.register') in self.driver.current_url

import time
from front_end_tests import TestBase, login
from flask import url_for, session, g
from flaskr.db import get_db

def login_and_create_post(self, title, body):
    login(self)
    self.driver.find_element_by_id("create_link").click()
    self.driver.find_element_by_id("title").send_keys(title)
    self.driver.find_element_by_id("body").send_keys(body)
    self.driver.find_element_by_id("submit_btn").click()


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
        # assert self.driver.find_element_by_id("create_link") is None

        login(self, "test", "test")
        self.driver.find_element_by_id("flaskr_btn").click()
        assert self.driver.find_element_by_id("logout_link")


    def test_create_post(self):
        """
        Tests that a user can create a post when logged in, after post is saved
        that the user is redirected to the home page
        """
        login_and_create_post(self, "New Title test", "New body test")
        assert url_for('blog.index') in self.driver.current_url
        # TODO: check for the post at home page


    def test_create_post_no_title(self):
        """
        Tests that the post form is not sent if the title is empty
        """
        login_and_create_post(self, "", "New test body")
        assert url_for("blog.create") in self.driver.current_url


    def test_create_post_no_body(self):
        """
        Tests that the post form is not sent if the body is empty
        """
        login_and_create_post(self, "New title test", "")
        assert url_for("blog.create") in self.driver.current_url


    def test_create_post_no_body_no_title(self):
        """
        Tests that the post form is not sent if the body and title are empty
        """
        login_and_create_post(self, "", "")
        assert url_for("blog.create") in self.driver.current_url


    # TODO:
    def test_create_comment(self):
        # login(self)
        self.driver.find_element_by_id("flaskr_btn").click()
        self.driver.find_element_by_id("comments_link").click()
        # assert url_for("blog.comment") in self.driver.current_url

        self.driver.find_element_by_id("comment").send_keys("Testing comment")
        self.driver.find_element_by_id("submit_btn").click()


    def test_delete_post(self):
        """
        Tests that a logged in user is able to delete their posts and is
        redirected home after
        """
        login(self)
        self.driver.find_element_by_id("edit_link").click()
        # TODO: asssert redirected
        self.driver.find_element_by_id("delete_btn").click()
        assert url_for("blog.index") in self.driver.current_url

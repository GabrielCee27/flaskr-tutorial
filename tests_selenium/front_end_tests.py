import unittest
import urllib2

import os
import tempfile

from flask_testing import LiveServerTestCase
from selenium import webdriver

from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

db_fd, db_path = tempfile.mkstemp()

class TestBase(LiveServerTestCase):

    def create_app(self):
        # db_fd, db_path = tempfile.mkstemp()

        app = create_app({
            'TESTING': True,
            'DATABASE': db_path,
        })

        with app.app_context():
            init_db()
            get_db().executescript(_data_sql)

        return app


    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

        # with app.app_context():
        #     init_db()
        #     get_db().executescript(_data_sql)


    def tearDown(self):
        os.close(db_fd)
        os.unlink(db_path)
        self.driver.quit()


    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


    if __name__ == '__main__':
        unittest.main()


# import time
# from flask import url_for
#
# class TestRegistration(TestBase):
#
#     def test_registration(self):
#         self.driver.find_element_by_id("registration_link").click()
#         time.sleep(1)
#

import pytest
import time
from flask import g, session, url_for
from flaskr.db import get_db
from selenium.webdriver.support.ui import WebDriverWait

# @pytest.mark.usefixtures("driver")
# class TestRegistration:
#     def test_register(self):
#         time.sleep(5)

def test_load(driver):
    driver.get("http://localhost:5000/")
    time.sleep(4)


# @pytest.mark.usefixtures("app")
# class BaseTest:
    # pass
#
#
# class TestRegistration(BaseTest):
#     def test_load(self):
#         wait = WebDriverWait(self.driver, 3)
#         self.driver.get("http://localhost:5000")
#         time.sleep(4)

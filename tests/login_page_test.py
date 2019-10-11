# Ranorex Webtestit Test File

import csv
from parameterized import parameterized

from utils.base_test import BaseTest
from pageobjects.login_page_object import LoginPageObject

with open("./data/data.csv") as data_file:
    TEST_DATA = [tuple(line) for line in csv.reader(data_file)]


def custom_name_func(testcase_func, _param_num, param):
    return "%s [Username: '%s'; Pass: '%s']" % (
        testcase_func.__name__, parameterized.to_safe_name(
            param.args[0]), parameterized.to_safe_name(param.args[1]))


class LoginPageTest(BaseTest):
    @parameterized.expand(TEST_DATA, testcase_func_name=custom_name_func)
    def test_sample_case(self, username, password, should_pass):
        driver = self.get_driver()

        # Initiating the Page Object
        login_po = LoginPageObject(driver)

        # Open the Web Page
        login_po.open("https://the-internet.herokuapp.com/login")

        # Enter the username, password and click on login
        login_po.enter_username(username).enter_password(
            password).click_login()

        # Capture the login message after clicking the button
        result_message = login_po.get_login_message()

        # Indicate what username/password combination was used in failure case
        iteration_indicator = "For username '{0}' and pass '{1}', ".format(
            username, password)

        self.assertEqual(
            result_message,
            "You logged into a secure area!"
            if should_pass == "true" else "Your username is invalid!",
            msg=iteration_indicator)

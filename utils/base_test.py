import unittest
import os
import hashlib
from utils.driver_setup import DriverSetup


class BaseTest(unittest.TestCase):
    def setUp(self):
        execution_type = os.environ.get("RX_ENDPOINT_TYPE")
        browser_name = os.environ.get("RX_ENDPOINT_BROWSER")

        if execution_type == "seleniumgrid":
            self.driver = DriverSetup().get_selenium_grid_driver(browser_name)
        elif execution_type == "local":
            self.driver = DriverSetup().get_local_driver(browser_name)
        elif execution_type == "android":
            self.driver = DriverSetup().get_chrome_android_driver()
        elif execution_type == "custom":
            self.driver = DriverSetup().get_custom_driver()
        elif execution_type == "saucelabs":
            self.driver = DriverSetup().get_saucelabs_driver(browser_name)

    def tearDown(self):
        if os.environ.get("RX_SCREENSHOT_ON_FAILURE"
                          ) == "True" and not self._is_success():
            description = self.__class__.__name__ + self._testMethodName
            name_hash = hashlib.md5(description.encode("utf-8")).hexdigest()
            filename = 'reports/screenshots/{0}-{1}-{2}.jpg'.format(
                os.environ.get("RX_TIMESTAMPSTARTED"),
                os.environ.get("RX_ENDPOINT_BROWSER"), name_hash)
            os.makedirs("reports/screenshots", exist_ok=True)
            self.driver.get_screenshot_as_file(filename)

        if os.environ.get("RX_DEBUG") != "True":
            self.driver.quit()

    def get_driver(self):
        return self.driver

    def _is_success(self):
        if hasattr(self, "_outcome"):
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, self._outcome.errors)

        error = self._list2reason(result.errors)
        failure = self._list2reason(result.failures)

        return not error and not failure

    def _list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
        return None

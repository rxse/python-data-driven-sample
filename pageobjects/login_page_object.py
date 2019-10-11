# Ranorex Webtestit Page Object File

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Additional data: {"img":"screenshots/9b0a8b43-047d-9fc2-64d1-f3ba0dab2db6.png"}
class LoginPageObject:
    """
    NOTE: Use Ranorex Selocity or the Elements Panel to generate element code
    """
    # Additional data:
    # {"img":"screenshots/b7dd8dbd-94d9-f53e-7794-bc69f5e63951.png"}
    _username = (By.CSS_SELECTOR, "#username")
    # Additional data:
    # {"img":"screenshots/36366582-8046-7168-e2b3-c6172a95b2ea.png"}
    _password = (By.CSS_SELECTOR, "#password")
    # Additional data:
    # {"img":"screenshots/13113c31-f167-d032-a3b0-c4c36bcd59dd.png"}
    _login = (By.CSS_SELECTOR, "[class='fa fa-2x fa-sign-in']")
    # Additional data:
    # {"img":"screenshots/2ff364ca-d546-0135-b8e0-555335c2ba8a.png"}
    _result_message = (By.CSS_SELECTOR, "#flash")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        return self

    def get_title(self):
        return self.driver.title

    """
    NOTE: Drag elements from the Elements panel into the code editor to
    generate methods. Drag elements into existing methods to add steps.
    """
    def enter_username(self, text):
        self.wait.until(EC.visibility_of_element_located(
            self._username)).send_keys(text)

        return self

    def enter_password(self, text):
        self.wait.until(EC.visibility_of_element_located(
            self._password)).send_keys(text)

        return self

    def click_login(self):
        self.wait.until(EC.visibility_of_element_located(self._login)).click()

        return self

    def get_login_message(self):
        login_message = self.wait.until(
            EC.visibility_of_element_located(
                self._result_message)).text.replace("×", "").strip()

        return login_message

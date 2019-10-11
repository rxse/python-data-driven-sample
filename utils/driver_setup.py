import os
import json
import types
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from dict_recursive_update import recursive_update


class DriverSetup():
    def __init__(self):
        self.driver = None

    def get_local_driver(self, browsername):
        exec_path = os.environ.get("RX_ENDPOINT_DRIVER_PATH")
        capabilities = self._parse_desired_caps(
            os.environ.get("RX_ENDPOINT_CAPABILITIES"))
        caps = self._generate_browser_caps(capabilities)
        self._add_proxy_support(caps)

        if browsername == "firefox":
            self.driver = webdriver.Firefox(
                executable_path=exec_path,
                desired_capabilities=caps["firefox"])
        elif browsername == "chrome":
            self.driver = webdriver.Chrome(executable_path=exec_path,
                                           desired_capabilities=caps["chrome"])
        elif browsername == "MicrosoftEdge":
            self.driver = webdriver.Edge(capabilities=caps["MicrosoftEdge"])
        elif browsername == "internet explorer":
            self.driver = webdriver.Ie(
                executable_path=exec_path,
                desired_capabilities=caps["internet explorer"])
        elif browsername == "safari":
            self.driver = webdriver.Safari(desired_capabilities=caps["safari"])
        elif browsername == "opera":
            self.driver = webdriver.Opera(executable_path=exec_path,
                                          desired_capabilities=caps["opera"])
        else:
            self.driver = webdriver.Chrome(executable_path=exec_path,
                                           desired_capabilities=caps["chrome"])

        self._override_service_destructor()

        return self.driver

    def get_selenium_grid_driver(self, browsername):
        capabilities = self._parse_desired_caps(
            os.environ.get("RX_ENDPOINT_CAPABILITIES"))
        capabilities["browserName"] = browsername
        capabilities["platform"] = os.environ.get("RX_ENDPOINT_PLATFORM")
        capabilities["version"] = os.environ.get("RX_ENDPOINT_VERSION")
        caps = self._generate_browser_caps(capabilities)
        self._add_proxy_support(caps)

        self.driver = webdriver.Remote(
            command_executor=os.environ.get("RX_ENDPOINT_GRID_URL"),
            desired_capabilities=caps[browsername])

        return self.driver

    def get_custom_driver(self):
        capabilities = self._parse_desired_caps(
            os.environ.get("RX_ENDPOINT_CAPABILITIES"))
        self._add_proxy_support(capabilities)

        self.driver = webdriver.Remote(
            command_executor=os.environ.get("RX_ENDPOINT_GRID_URL"),
            desired_capabilities=capabilities)

        return self.driver

    def get_chrome_android_driver(self):
        capabilities = self._parse_desired_caps(
            os.environ.get("RX_ENDPOINT_CAPABILITIES"))
        caps = self._generate_browser_caps(capabilities)
        caps["chrome"]["goog:chromeOptions"]["androidPackage"] = "com.android.chrome"
        self._add_proxy_support(caps)

        self.driver = webdriver.Chrome(
            executable_path=os.environ.get("RX_ENDPOINT_DRIVER_PATH"),
            desired_capabilities=caps["chrome"])

        self._override_service_destructor()

        return self.driver

    def get_saucelabs_driver(self, browser_name):
        capabilities = self._parse_desired_caps(
            os.environ.get("RX_ENDPOINT_CAPABILITIES"))

        capabilities["username"] = os.environ.get("RX_ENDPOINT_USER")
        capabilities["accessKey"] = os.environ.get("RX_ENDPOINT_KEY")
        capabilities["platform"] = os.environ.get("RX_ENDPOINT_PLATFORM")
        capabilities["browserName"] = browser_name
        capabilities["version"] = os.environ.get("RX_ENDPOINT_VERSION")
        self._add_proxy_support(capabilities)

        self.driver = webdriver.Remote(
            command_executor=os.environ.get("RX_ENDPOINT_GRID_URL"),
            desired_capabilities=capabilities)

        return self.driver

    def _generate_browser_caps(self, capabilities):
        caps = dict()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = os.environ.get(
            "RX_ENDPOINT_HEADLESS") == "True"
        if os.environ.get(
                "RX_DEBUG") == "True" and "RX_SELOCITYPATH" in os.environ:
            chrome_options.add_argument("--load-extension=" +
                                        os.environ.get("RX_SELOCITYPATH"))
            chrome_options.add_argument("--auto-open-devtools-for-tabs")
            chrome_options.add_experimental_option(
                "prefs",
                {"devtools.preferences.currentDockState": "\"undocked\""})
        caps["chrome"] = recursive_update(chrome_options.to_capabilities(),
                                          capabilities)

        caps["opera"] = recursive_update(
            {"operaOptions": {
                "binary": os.environ.get("RX_OPERA_PATH")
            }}, capabilities)
        caps["safari"] = capabilities
        caps["internet explorer"] = capabilities
        caps["MicrosoftEdge"] = capabilities

        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = os.environ.get(
            "RX_ENDPOINT_HEADLESS") == "True"
        caps["firefox"] = recursive_update(firefox_options.to_capabilities(),
                                           capabilities)

        return caps

    def _parse_desired_caps(self, caps: str):
        try:
            json_object = json.loads(
                caps.replace("chromeOptions", "goog:chromeOptions").replace(
                    "firefoxOptions", "moz:firefoxOptions"))
            return json_object
        except ValueError:
            return None

    def _override_service_destructor(self):
        if "RX_DEBUG" in os.environ and os.environ.get(
                "RX_DEBUG") == "True" and hasattr(self.driver, "service"):
            self.driver.service.__class__.__base__.__del__ = types.MethodType(
                debug_destructor, self.driver.service.__class__.__base__)

    def _add_proxy_support(self, capabilities):
        if "RX_PROXY" in os.environ:
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = os.environ.get("RX_PROXY")
            proxy.socks_proxy = os.environ.get("RX_PROXY")
            proxy.ssl_proxy = os.environ.get("RX_PROXY")
            proxy.add_to_capabilities(capabilities)


def debug_destructor(_self):
    try:
        print("Browser cleanup interrupted by Debug mode")
    # pylint: disable=broad-except
    except Exception:
        pass

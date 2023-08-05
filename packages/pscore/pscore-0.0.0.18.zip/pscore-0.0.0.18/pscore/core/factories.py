from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from pscore.config.test_configuration import TestConfiguration
from pscore.core.event_listeners import DefaultWebDriverEventListener
from pscore.core.wd_extensions import WebDriverExtensions
from pscore.core.drivers.driver_helper import ChromeDriverHelper, IEDriverHelper
from .drivers.skygrid_driver import SkygridDriver

BROWSER_IE = 'ie'
BROWSER_CHROME = 'chrome'
BROWSER_FIREFOX = 'firefox'
BROWSER_IPHONE = 'iphone'
BROWSER_IPAD = 'ipad'
BROWSER_ANDROID = 'android'
BROWSER_SAFARI = 'safari'

ENVIRONMENT_GRID = 'grid'
ENVIRONMENT_LOCAL = 'local'
ENVIRONMENT_AMAZON = 'amazon'
ENVIRONMENT_SAUCELABS = 'saucelabs'

SAUCELABS_HUB_URL = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"


class WebDriverFactory(object):
    @staticmethod
    def get_local_driver(desired_browser, driver, logger):
        print('Driver Factory: Initializing driver for the local environment')
        print('Driver Factory: Initializing ' + desired_browser + ' browser')
        if desired_browser == BROWSER_FIREFOX:
            driver = webdriver.Firefox()
        elif desired_browser == BROWSER_CHROME:
            driver = webdriver.Chrome(executable_path=ChromeDriverHelper.get_chromedriver())
        elif desired_browser == BROWSER_ANDROID:
            chrome_package = TestConfiguration.get_chrome_package_name()
            caps = {'chromeOptions': {'androidPackage': chrome_package}}
            driver = webdriver.Chrome(executable_path=ChromeDriverHelper.get_chromedriver(), desired_capabilities=caps)
        elif desired_browser == BROWSER_IE:
            driver_path = IEDriverHelper.get_ie_driver()
            driver = webdriver.Ie(executable_path=driver_path)
        else:
            logger.error("Specified browser not recognised: " + desired_browser)
            raise RuntimeError(
                "Specified browser not recognised: " + desired_browser)
        return driver

    @staticmethod
    def get_amazon_driver(desired_browser, driver, logger):
        logger.info(
            'Driver Factory: Initializing driver for amazon grid: ' + TestConfiguration.get_amazon_hub_url())
        logger.info('Driver Factory: Initializing ' + desired_browser + ' browser')
        driver = webdriver.Remote(
            command_executor=TestConfiguration.get_amazon_hub_url(),
            desired_capabilities={
                "browserName": "firefox",
                "version": TestConfiguration.get_browser_version(),
                "video": "True",
                "platform": "WIN8",
            })
        print(
            "Video: https://s3-eu-west-1.amazonaws.com/be8f5d0a-c2d2-9383-27b0-464cabf83d80/e324de1a-1345-dc16-cb76-8477d39c4376/play.html?" + driver.session_id)
        return driver

    @staticmethod
    def get_grid_driver(desired_browser, driver, logger):
        logger.info('Driver Factory: Initializing driver for grid: ' + TestConfiguration.get_hub_url())
        logger.info('Driver Factory: Initializing ' + desired_browser + ' browser')
        browser = 'internet explorer' if desired_browser == BROWSER_IE else desired_browser
        desired_caps = dict(browserName=browser, environment=TestConfiguration.get_user_id())
        driver = webdriver.Remote(command_executor=TestConfiguration.get_hub_url(), desired_capabilities=desired_caps)
        return driver

    @staticmethod
    def get_skygrid_driver(desired_browser, driver, test_context):
        test_context.logger.info('Creating driver for Skygrid')
        browser = 'internet explorer' if desired_browser == BROWSER_IE else desired_browser
        driver = SkygridDriver(command_executor=TestConfiguration.get_hub_url(),
                               desired_capabilities=dict(browserName=browser,
                                                         environment=TestConfiguration.get_user_id()))
        # driver needs a reference to the test context for saving screenshots
        driver.test_context = test_context
        test_context.start_timer()
        return driver

    @staticmethod
    def get(logger, test_name="Python core framework", test_context=None):
        """
        This function constructs a webdriver instance based on the configuration env var values stored in the local
        machine.

        The returned driver will be configured for either a local, Saucelabs, Selenium Grid or AWS Grid environment.

        The environment variables queried are covered in the package readme.

        :rtype : selenium.webdriver.remote.webdriver.WebDriver
        """

        driver = None

        desired_execution_environment = TestConfiguration.get_execution_environment()
        desired_browser = TestConfiguration.get_browser()
        desired_browser_version = TestConfiguration.get_browser_version()

        if desired_execution_environment == ENVIRONMENT_LOCAL:
            driver = WebDriverFactory.get_local_driver(desired_browser, driver, logger)

        elif desired_execution_environment == ENVIRONMENT_AMAZON:
            driver = WebDriverFactory.get_amazon_driver(desired_browser, driver, logger)

        elif desired_execution_environment == ENVIRONMENT_GRID:
            if TestConfiguration.get_skygrid_enabled():
                driver = WebDriverFactory.get_skygrid_driver(desired_browser, driver, test_context)
            else:
                driver = WebDriverFactory.get_grid_driver(desired_browser, driver, logger)

        elif desired_execution_environment in [ENVIRONMENT_SAUCELABS, 'sauce']:
            driver = WebDriverFactory.get_saucelabs_driver(logger, test_name, desired_browser, desired_browser_version)

        else:
            logger.error("Specified execution environment not recognised: " + desired_execution_environment)
            raise RuntimeError(
                "Specified execution environment not recognised: " + desired_execution_environment)

        if desired_browser not in [BROWSER_IPHONE, BROWSER_IPAD, BROWSER_ANDROID]:
            logger.info("maxing the screen")
            driver.maximize_window()

        # Now the nature of the driver has been established we want to add in our extension methods
        driver = WebDriverExtensions.patch(driver)
        driver = EventFiringWebDriver(driver, DefaultWebDriverEventListener(logger))

        return driver

    @staticmethod
    def get_saucelabs_driver(logger, test_name, browser, version=None):
        sauce_url = SAUCELABS_HUB_URL % (
            TestConfiguration.get_sauce_username(), TestConfiguration.get_sauce_key())

        try:
            windows = 'windows 7'
            if browser in [BROWSER_FIREFOX, BROWSER_CHROME]:
                caps = WebDriverFactory.saucelabs_caps(browser, windows, version, screen_res="1280x1024")
            elif browser == BROWSER_IE:
                caps = WebDriverFactory.saucelabs_caps("internet explorer", windows, version,
                                                       screen_res="1280x1024")
            elif browser in [BROWSER_IPAD, BROWSER_IPHONE]:
                caps = WebDriverFactory.sauce_ios_caps(browser, version)
            elif browser in [BROWSER_ANDROID]:
                caps = WebDriverFactory.sauce_android_caps(version)
            elif browser in [BROWSER_SAFARI]:
                caps = WebDriverFactory.sauce_safari_caps(version)
            else:
                raise Exception("Unknown browser requested for saucelabs")

            caps['name'] = test_name

            parent_account = TestConfiguration.get_sauce_parent_account()
            if TestConfiguration.get_sauce_username() != parent_account:
                caps['parent-tunnel'] = parent_account

            tunnel_id = TestConfiguration.get_sauce_tunnel_id()
            caps['tunnel-identifier'] = tunnel_id

            driver = webdriver.Remote(
                desired_capabilities=caps,
                command_executor=sauce_url
            )
            return driver
        except Exception as e:
            logger.error("HTTPError raised while trying to connect to SauceLabs:\n {0} {1}".format(str(e), sauce_url))
            logger.error("Exception raised while trying to initialise a driver for SauceLabs: " + str(e))
            raise

    @staticmethod
    def saucelabs_caps(browser_name, platform, version, screen_res=None):
        caps = {'browserName': browser_name, 'platform': platform, 'version': version}
        if screen_res:
            caps['screen-resolution'] = screen_res

        return caps

    @staticmethod
    def sauce_ios_caps(browser, version, logger):
        if version is None or version == '':
            version = '8.1'
            logger.warning("You did not specify an iOS version. We are giving you {}".format(version))

        caps = {
            'browserName': 'safari',
            'appiumVersion': "",
            'platformVersion': version,
            'platformName': 'iOS',
            'newCommandTimeout': 180,
            'safariAllowPopups': 'true',
            'command-timeout': 180,
            'idle-timeout': 180
        }
        if browser in [BROWSER_IPHONE]:
            caps['deviceName'] = "iPhone Simulator"
            caps['device-orientation'] = 'portrait'
        else:
            caps['deviceName'] = "iPad Simulator"
            caps['device-orientation'] = 'landscape'
        return caps

    @staticmethod
    def sauce_android_caps(version):
        if version.lower() == 'beta':
            caps = {
                'platformName': 'Android',
                'deviceName': 'Samsung Galaxy S4 Device',
                'platformVersion': '4.3',
                'browserName': 'Chrome',
                'appium-version': ""
            }
        else:
            caps = {
                'platform': 'Linux',
                'version': version,
                'deviceName': 'Android Emulator',
                'browserName': 'Android',
                'javascriptEnabled': True,
            }

        caps['newCommandTimeout'] = 180
        caps['device-orientation'] = 'portrait'
        return caps

    @staticmethod
    def sauce_safari_caps(version):
        if version is None or version == '':
            version = '8'

        browser_os_map = {
            '8': 'OS X 10.10',
            '7': 'OS X 10.9',
            '6': 'OS X 10.8',
            '5': 'OS X 10.7'
        }
        os_version = browser_os_map[version]

        caps = {
            'browserName': 'safari',
            'platform': os_version,
            'version': version,
            'screen-resolution': '1024x768'
        }
        return caps

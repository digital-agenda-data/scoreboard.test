import os
import unittest
from selenium.webdriver.remote.webdriver import WebDriver


class BrowserTestCase(unittest.TestCase):

    browser = None
    url = None

    def __init__(self, methodName, browser: WebDriver, url: str):
        super().__init__(methodName)
        self.browser = browser
        self.url = url

    @classmethod
    def my_tests(cls):
        return unittest.defaultTestLoader.getTestCaseNames(cls)

    def screenshot(self, suffix: str = ''):
        suffix = suffix or self._get_screenshot_suffix()
        name = '{}/screenshot_{}.png'.format(os.getcwd(), suffix)
        self.browser.save_screenshot(name)
        print('Saved {}.'.format(name))

    def _get_screenshot_suffix(self) -> str:
        return '_'.join(self.browser.current_url.split('/')[2:])


class BrowserTestResult(unittest.runner.TextTestResult):
    def addFailure(self, test: BrowserTestCase, err):
        test.screenshot()
        super().addFailure(test, err)

    def addError(self, test: BrowserTestCase, err):
        test.screenshot()
        super().addError(test, err)

    def getDescription(self, test: BrowserTestCase):
        text = super().getDescription(test)
        return '[{}] {}'.format(test.browser.current_url, text)

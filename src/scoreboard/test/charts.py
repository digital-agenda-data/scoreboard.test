import unittest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from scoreboard.test.common import BrowserTestCase


CSS_SELECTOR_DATASETS = '.dataset-description-area > a'
CSS_SELECTOR_CHARTS = '.scoreboard-visualizations-listing .thumbnail-area a'

ID_CHART = 'the-chart'
CSS_SELECTOR_CHART_LOADING = '#{}.loading-small'.format(ID_CHART)

TIMEOUT_CHART = 10
MSG_TIMEOUT_CHART = '[{}] Chart failed to load in {} seconds!'


def suite(browser: WebDriver, base_url):
    browser.get(base_url)
    datasets = browser.find_elements_by_css_selector(CSS_SELECTOR_DATASETS)

    test_suite = unittest.TestSuite()

    for dataset_url in [dataset.get_attribute('href') for dataset in datasets]:
        browser.get(dataset_url)
        charts = browser.find_elements_by_css_selector(CSS_SELECTOR_CHARTS)

        for chart in charts:
            for name in TableTestCase.my_tests():
                testcase = TableTestCase(
                    name, browser, chart.get_attribute('href'))
                test_suite.addTest(testcase)

    return test_suite


class TableTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)
        WebDriverWait(self.browser, TIMEOUT_CHART).until(
            lambda d: (
                not d.find_elements_by_css_selector(CSS_SELECTOR_CHART_LOADING)
            ), message=MSG_TIMEOUT_CHART.format(self.url, TIMEOUT_CHART)
        )

    def test_chart_exists(self):
        """ Chart container exists. """
        try:
            chart = self.browser.find_element_by_id(ID_CHART)
        except NoSuchElementException:
            chart = None

        fail_msg = "[{}] Can't find .{}!".format(self.url, ID_CHART)
        self.assertNotEqual(chart, None, fail_msg)

    def test_chart_content(self):
        """ Chart svg has child elements. """
        svg = self.browser.find_element_by_tag_name('svg')
        contents = svg.find_elements_by_xpath('*')

        fail_msg = '[{}] {} appears to be empty!'.format(self.url, ID_CHART)
        self.assertGreater(len(contents), 0, fail_msg)

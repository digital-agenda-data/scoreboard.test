import unittest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from scoreboard.test.common import BrowserTestCase


CSS_SELECTOR_DATASETS = '.dataset-description-area > a'
CSS_SELECTOR_CHARTS = '.scoreboard-visualizations-listing .thumbnail-area a'

ID_CHART = 'the-chart'
CSS_SELECTOR_CHART_LOADING = '#{}.loading-small'.format(ID_CHART)
CSS_SELECTOR_CHART_CONTENT = '#{chart_id} svg, #{chart_id} table'.format(
    chart_id=ID_CHART
)

TIMEOUT_CHART = 10
MSG_TIMEOUT_CHART = 'Chart failed to load in {} seconds!'.format(TIMEOUT_CHART)


def suite(browser: WebDriver, base_url):
    browser.get(base_url)
    datasets = browser.find_elements_by_css_selector(CSS_SELECTOR_DATASETS)

    test_suite = unittest.TestSuite()

    for dataset_url in [dataset.get_attribute('href') for dataset in datasets]:
        browser.get(dataset_url)
        charts = browser.find_elements_by_css_selector(CSS_SELECTOR_CHARTS)

        for chart in charts:
            for name in ChartsTestCase.my_tests():
                testcase = ChartsTestCase(
                    name, browser, chart.get_attribute('href'))
                test_suite.addTest(testcase)

    return test_suite


class ChartsTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)
        wait = WebDriverWait(self.browser, TIMEOUT_CHART)
        wait.until(_check_chart_loading, message=MSG_TIMEOUT_CHART)

    def test_chart_exists(self):
        """ Chart container exists. """
        try:
            chart = self.browser.find_element_by_id(ID_CHART)
        except NoSuchElementException:
            chart = None

        self.assertTrue(chart, 'Can\'t find "{}"!'.format(ID_CHART))

    def test_chart_content(self):
        """ Chart svg has child elements. """
        try:
            svg = self.browser.find_element_by_css_selector(
                CSS_SELECTOR_CHART_CONTENT)
        except NoSuchElementException:
            svg = None

        self.assertTrue(svg, 'Can\'t find "{}"!'.format(
            CSS_SELECTOR_CHART_CONTENT))

        contents = svg.find_elements_by_xpath('*')

        fail_msg = '"{}" appears to be empty!'.format(
            self.url, CSS_SELECTOR_CHART_CONTENT)

        self.assertGreater(len(contents), 0, fail_msg)


def _check_chart_loading(browser):
    return not browser.find_elements_by_css_selector(
        CSS_SELECTOR_CHART_LOADING
    )

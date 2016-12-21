import argparse
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from scoreboard.test import config


class IndicatorTableTestCase(unittest.TestCase):

    browser = None
    url = None

    def __init__(self, methodName, browser, url):
        super().__init__(methodName)
        self.browser = browser
        self.url = url

    @classmethod
    def my_tests(cls):
        return unittest.defaultTestLoader.getTestCaseNames(cls)

    def setUp(self):
        self.browser.get(self.url)

    def test_table_exists(self):
        try:
            table = self.browser.find_element_by_class_name(
                config.CSS_CLASS_INDICATORS_TABLE
            )
        except NoSuchElementException:
            table = None

        fail_msg = "[{}] Can't find .{}!".format(
            self.url, config.CSS_CLASS_INDICATORS_TABLE
        )
        self.assertNotEqual(table, None, fail_msg)

    def test_table_rows(self):
        table = self.browser.find_element_by_class_name(
            config.CSS_CLASS_INDICATORS_TABLE
        )
        rows = table.find_elements_by_tag_name('tr')

        fail_msg = '[{}] {} has too few rows!'.format(
            self.url, config.CSS_CLASS_INDICATORS_TABLE)

        self.assertGreaterEqual(len(rows), 2, fail_msg)


def suite(browser, base_url, section=config.DATASETS_SECTION):
    browser.get('{}/{}'.format(base_url, section))
    datasets = browser.find_elements_by_link_text(
        config.TEXT_DATASET_INDICATORS_HREF
    )

    test_suite = unittest.TestSuite()

    for dataset in datasets:

        cls = IndicatorTableTestCase

        for name in cls.my_tests():
            testcase = cls(name, browser, dataset.get_attribute('href'))
            test_suite.addTest(testcase)

    return test_suite


def run(base_url, verbosity=1):
    browser = webdriver.Chrome()
    test_runner = unittest.TextTestRunner(verbosity=verbosity)
    test_suite = suite(browser, base_url)
    test_runner.run(test_suite)
    browser.quit()


def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', type=str)
    parser.add_argument('-v', '--verbose', action='count', default=1)
    args = parser.parse_args()
    run(args.URL, args.verbose)

if __name__ == '__main__':
    run_cli()

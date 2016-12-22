import unittest
from selenium.common.exceptions import NoSuchElementException
from scoreboard.test.common import BrowserTestCase


CSS_CLASS_INDICATORS_TABLE = 'list_indicators'
TEXT_DATASET_INDICATORS_HREF = (
    'Consult the list of indicators, their definition and sources'
)


def suite(browser, base_url):
    browser.get(base_url)
    datasets = browser.find_elements_by_link_text(TEXT_DATASET_INDICATORS_HREF)

    test_suite = unittest.TestSuite()

    for dataset in datasets:

        for name in TableTestCase.my_tests():
            testcase = TableTestCase(
                name, browser, dataset.get_attribute('href'))
            test_suite.addTest(testcase)

    return test_suite


class TableTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    def test_table_exists(self):
        """ Table exists. """
        try:
            table = self.browser.find_element_by_class_name(
                CSS_CLASS_INDICATORS_TABLE
            )
        except NoSuchElementException:
            table = None

        fail_msg = "[{}] Can't find .{}!".format(
            self.url, CSS_CLASS_INDICATORS_TABLE
        )
        self.assertNotEqual(table, None, fail_msg)

    def test_table_rows(self):
        """ Table has acceptable number of rows. """
        table = self.browser.find_element_by_class_name(
            CSS_CLASS_INDICATORS_TABLE
        )
        rows = table.find_elements_by_tag_name('tr')

        fail_msg = '[{}] {} has too few rows!'.format(
            self.url, CSS_CLASS_INDICATORS_TABLE)

        self.assertGreaterEqual(len(rows), 2, fail_msg)

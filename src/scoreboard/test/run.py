import argparse
import inspect
import unittest
from selenium import webdriver


class IndicatorTableTestCase(unittest.TestCase):

    browser = None
    dataset_indicators_url = None
    _table_class = 'list_indicators'

    def setUp(self):
        self.browser.get(self.dataset_indicators_url)

    def test_table_exists(self):
        table = self.browser.find_element_by_class_name(self._table_class)
        self.assertNotEqual(
            table, None,
            "[{}] Can't find .{}!".format(
                self.dataset_indicators_url,
                self._table_class
            )
        )

    def test_table_rows(self):
        table = self.browser.find_element_by_class_name(self._table_class)
        rows = table.find_elements_by_tag_name('tr')
        self.assertGreaterEqual(
            len(rows), 2,
            '[{}] {} has too few rows!'.format(
                self.dataset_indicators_url,
                self._table_class
            )
        )


def suite(browser, base_url, section='datasets'):
    browser.get('{}/{}'.format(base_url, section))
    datasets = browser.find_elements_by_link_text(
        'Consult the list of indicators, their definition and sources')

    test_suite = unittest.TestSuite()

    for dataset in datasets:
        members = inspect.getmembers(
            IndicatorTableTestCase(),
            predicate=inspect.ismethod
        )

        for name, _ in members:
            if not name.startswith('test'):
                continue

            testcase = IndicatorTableTestCase(name)

            testcase.browser = browser
            testcase.dataset_indicators_url = dataset.get_attribute('href')

            test_suite.addTest(testcase)

    return test_suite


def run(base_url):
    browser = webdriver.Chrome()
    unittest.TextTestRunner(verbosity=2).run(suite(browser, base_url))
    browser.quit()


def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', type=str)
    args = parser.parse_args()
    run(args.URL)

if __name__ == '__main__':
    run_cli()

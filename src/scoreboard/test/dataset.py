from urllib import request
import unittest
from selenium.common.exceptions import NoSuchElementException
from scoreboard.test.common import BrowserTestCase


ID_METADATA = 'dataset-metadata'
ID_DIMENSIONS = 'dataset-dimensions'

TEXT_DATASET_PAGE_HREF = (
    'Entire dataset metadata and download services'
)

TEXT_CSV_DOWNLOAD = 'CSV'
TEXT_TSV_DOWNLOAD = 'TSV'
TEXT_N3_DOWNLOAD = 'N3/Turtle'
TEXT_HTML_DOWNLOAD = 'HTML'

TEXT_CODELISTS_DOWNLOAD = 'Codelists'
TEXT_STRUCTURE_DOWNLOAD = 'Dataset metadata and structure'


def suite(browser, base_url):
    browser.get(base_url)
    datasets = browser.find_elements_by_link_text(TEXT_DATASET_PAGE_HREF)

    test_suite = unittest.TestSuite()

    for dataset in datasets:

        for name in DatasetTestCase.my_tests():
            testcase = DatasetTestCase(
                name, browser, dataset.get_attribute('href'))
            test_suite.addTest(testcase)

    return test_suite


class DatasetTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    def test_metadata(self):
        """ Metadata section exists and has enough children. """

        section = self.browser.find_element_by_id(ID_METADATA)
        children = section.find_elements_by_xpath('*')

        self.assertGreater(len(children), 2)

    def test_dimensions(self):
        """ Dimensions section exists and has enough children. """

        section = self.browser.find_element_by_id(ID_DIMENSIONS)
        children = section.find_elements_by_tag_name('tr')

        self.assertGreater(len(children), 2)

    def test_download_csv(self):
        """ CSV download. """
        url = self.browser.find_element_by_link_text(TEXT_CSV_DOWNLOAD)
        resp = request.urlopen(url.get_attribute('href'))

        self.assertEqual(resp.getcode(), 200)
        self.assertEqual(resp.info().get_content_type(), 'application/zip')
        self.assertGreater(resp.length, 0)

    def test_download_tsv(self):
        """ TSV download. """
        url = self.browser.find_element_by_link_text(TEXT_TSV_DOWNLOAD)
        resp = request.urlopen(url.get_attribute('href'))

        self.assertEqual(resp.getcode(), 200)
        self.assertEqual(resp.info().get_content_type(), 'application/zip')
        self.assertGreater(resp.length, 0)

    def test_download_n3(self):
        """ N3/Turtle download. """
        url = self.browser.find_element_by_link_text(TEXT_N3_DOWNLOAD)
        resp = request.urlopen(url.get_attribute('href'))

        self.assertEqual(resp.getcode(), 200)
        # self.assertEqual(resp.info().get_content_type(), 'application/x-gzip')
        self.assertEqual(resp.info().get_content_type(), 'application/octet-stream')
        self.assertGreater(resp.length, 0)

    def test_download_html(self):
        """ HTML download. """
        url = self.browser.find_element_by_link_text(TEXT_HTML_DOWNLOAD)
        resp = request.urlopen(url.get_attribute('href'))

        self.assertEqual(resp.getcode(), 200)
        self.assertEqual(resp.info().get_content_type(), 'text/html')

    def test_download_codelists(self):
        """ Codelists download. """
        url = self.browser.find_element_by_link_text(TEXT_CODELISTS_DOWNLOAD)
        resp = request.urlopen(url.get_attribute('href'))

        self.assertEqual(resp.getcode(), 200)
        self.assertEqual(resp.info().get_content_type(), 'text/rdf+xml')
        self.assertEqual(resp.info().get_content_disposition(), 'attachment')
        self.assertTrue(resp.info().get_filename().endswith('-codelists.ttl'))

    def test_download_structure(self):
        """ Metadata and structure download. """
        url = self.browser.find_element_by_link_text(TEXT_STRUCTURE_DOWNLOAD)
        resp = request.urlopen(url.get_attribute('href'))

        self.assertEqual(resp.getcode(), 200)
        self.assertEqual(resp.info().get_content_type(), 'text/rdf+xml')
        self.assertEqual(resp.info().get_content_disposition(), 'attachment')
        self.assertTrue(resp.info().get_filename().endswith('-metadata.ttl'))

import argparse
import unittest
from selenium import webdriver
from scoreboard.test import indicators
from scoreboard.test import charts
from scoreboard.test import common

ARG_TESTS = {
    'indicators': indicators.suite,
    'charts': charts.suite,
}

MSG_UNKNOWN_TEST = (
    'Unknown test "{}"! '
    'Known tests: "{known_tests}"'
)

DRIVERS = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    'phantomjs': webdriver.PhantomJS,
    'edge': webdriver.Edge,
    'ie': webdriver.Ie,
    'safari': webdriver.Safari,
}


def _get_browser(name, path=None):
    browser = DRIVERS[name]
    return browser(executable_path=path) if path else browser()


def run(base_url, suite, verbosity=1, browser='chrome', browser_path=None):
    browser = _get_browser(browser, browser_path)
    test_runner = unittest.TextTestRunner(
        verbosity=verbosity,
        resultclass=common.BrowserTestResult
    )
    test_suite = suite(browser, base_url)
    test_runner.run(test_suite)
    browser.quit()


def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    parser.add_argument('test', nargs='+', type=str)
    parser.add_argument('-v', '--verbose', action='count', default=1)
    parser.add_argument('-B', '--browser', default='chrome')
    parser.add_argument('-P', '--browserpath', default=None)
    args = parser.parse_args()

    for test_name in args.test:
        assert test_name in ARG_TESTS, MSG_UNKNOWN_TEST.format(
            test_name, known_tests=', '.join(ARG_TESTS.keys()))
        suite = ARG_TESTS[test_name]
        run(args.url, suite, args.verbose, args.browser, args.browserpath)


if __name__ == '__main__':
    run_cli()

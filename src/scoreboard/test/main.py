import unittest
from scoreboard.test import common
from scoreboard.test import util


def run(base_url, suite, verbosity=1, browser='chrome', browser_path=None):
    browser = util.get_browser(browser, browser_path)
    test_runner = unittest.TextTestRunner(
        verbosity=verbosity,
        resultclass=common.BrowserTestResult
    )
    test_suite = suite(browser, base_url)
    test_runner.run(test_suite)
    browser.quit()


def run_cli():
    parser = util.build_cli_arguments()
    args = parser.parse_args()

    for test_name in args.test:
        util.validate_test_name(test_name)
        suite = util.ARG_TESTS[test_name]
        run(args.url, suite, args.verbose, args.browser, args.browserpath)

if __name__ == '__main__':
    run_cli()

import argparse
from selenium import webdriver
from scoreboard.test import indicators
from scoreboard.test import charts


ARG_TESTS = {
    'indicators': indicators.suite,
    'charts': charts.suite,
}


DRIVERS = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    'phantomjs': webdriver.PhantomJS,
    'edge': webdriver.Edge,
    'ie': webdriver.Ie,
    'safari': webdriver.Safari,
}


MSG_UNKNOWN_TEST = (
    'Unknown test "{}"! '
    'Known tests: "{known_tests}"'
)


def get_browser(name, path=None):
    browser = DRIVERS[name]
    return browser(executable_path=path) if path else browser()


def validate_test_name(test_name):
    assert test_name in ARG_TESTS, MSG_UNKNOWN_TEST.format(
        test_name, known_tests=', '.join(ARG_TESTS.keys()))


def build_cli_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            'Run tests on Scoreboard websites.\n'
            'The given browser webdriver must be in your $PATH\n'
            'or given via the --browserpath option.\n\n'
            'E.g.: chrome: chromedriver, firefox: geckodriver, '
            'edge: MicrosoftWebDriver.exe.'
        )
    )
    parser.add_argument(
        'url', type=str,
        help='Site url, eg: https://digital-agenda-data.eu.'
    )
    parser.add_argument(
        'test', nargs='*', type=str, default=ARG_TESTS.keys(),
        help='Test names, one or more of: "{}". Default: all'.format(
            ', '.join(ARG_TESTS.keys())
        )
    )
    parser.add_argument('-v', '--verbose', action='count', default=1)
    parser.add_argument(
        '-B', '--browser', default='chrome',
        help='Browser to use, known: "{}". Default: chrome'.format(
            ', '.join(DRIVERS.keys())
        )
    )
    parser.add_argument(
        '-P', '--browserpath', default=None,
        help='Custom path to browser executable.'
    )
    return parser

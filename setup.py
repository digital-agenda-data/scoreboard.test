# -*- coding: utf-8 -*-
"""Installer for the scoreboard.test package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='scoreboard.test',
    version='1.0a1',
    description="Selenium testing for Scoreboard.",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5.2",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='David Bătrânu',
    author_email='david.batranu@eaudeweb.ro',
    url='https://pypi.python.org/pypi/scoreboard.test',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['scoreboard'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'selenium>=3.0.2',
    ],
    entry_points={
        'console_scripts': ['scoreboard-test = scoreboard.test.run:run_cli']
    }
)

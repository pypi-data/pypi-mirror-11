#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys 
from setuptools import setup 
from setuptools.command.test import test as TestCommand 

class PyTest(TestCommand): 
    """
    pytest's integration with setuptools, which is borrowed from  
    http://pytest.org/latest/goodpractises.html#goodpractises
    """

    def finalize_options(self): 
        TestCommand.finalize_options(self)
        self.test_args = ['-s'] 
        self.test_suite = True 

    def run_tests(self): 
        import pytest 
        errcode = pytest.main(self.test_args) 
        sys.exit(errcode) 

setup(
    name = 'elogging', 
    url = 'https://github.com/my-zhang/elogging',
    version = '0.1.0', 
    license = 'Apache 2.0',
    author = 'Mengyu Zhang',
    author_email = 'mengyuzhang@uchicago.edu', 
    packages = ['elogging', 'elogging.handlers'], 
    install_requires = ['bernhard==0.2.4'],
    tests_require = ['pytest'], 
    cmdclass = {'test': PyTest}, 
    test_suite = 'test', 
    extras_require = {'testing': ['pytest']} 
)

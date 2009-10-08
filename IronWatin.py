#!/usr/bin/env ipy
import clr
clr.AddReference('WatiN.Core.dll')

# .NET imports
import WatiN.Core as Watin

# Python imports
import sys
sys.path.append('C:\Python26\Lib')

import time
import unittest

from optparse import OptionParser

class BrowserTest(unittest.TestCase):
    browser = None
    url = None
    def setUp(self):
        super(BrowserTest, self).setUp()
        if self.browser and self.url:
            self.browser = self.browser(self.url)

    def tearDown(self):
        if self.browser:
            if isinstance(self.browser, Watin.FireFox):
                # Firefox takes a sec to shut down :(
                time.sleep(1) 
            self.browser.Close()

        super(BrowserTest, self).tearDown()

class GoogleTest(BrowserTest):
    url = 'http://images.google.com'

    def runTest(self):
        print ('runTest', self.url, self.browser)

class _WatinTestResult(unittest._TextTestResult):
    def startTest(self, test):
        if self.browser:
            test.browser = self.browser
        if self.url:
            test.url = self.url
        unittest._TextTestResult.startTest(self, test)

class WatinTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        self.browser = kwargs.pop('browser', None)
        self.url = kwargs.pop('url', None)
        if self.browser:
            self.browser = self.browser == 'ie' and Watin.IE or Watin.FireFox
        unittest.TextTestRunner.__init__(self, *args, **kwargs)

    def _makeResult(self):
        rc = _WatinTestResult(self.stream, self.descriptions, self.verbosity)
        rc.browser = self.browser
        rc.url = self.url
        return rc

def main(options=None):
    op = options or OptionParser()
    op.add_option('-b', '--browser', dest='browser', default='ie', 
        help='Specify the browser to use [ie/firefox]')
    op.add_option('-u', '--url', dest='url', default='http://google.com', 
        help='Specify the URL to load in the browser')
    op.add_option('-v', '--verbose', dest='verbose', action='store_true')
    op.add_option('-q', '--quiet', dest='quiet', action='store_true')

    opts, args = op.parse_args()

    verbosity = 1
    if opts.quiet:
        verbosity = 0
    if opts.verbose:
        verbosity = 2

    tests = unittest.findTestCases(sys.modules[__name__])
    runner = WatinTestRunner(browser=opts.browser, url=opts.url, verbosity=verbosity)
    print ('tests', tests, type(tests))
    runner.run(tests)

if __name__ == '__main__':
    main()
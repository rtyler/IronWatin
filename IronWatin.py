#!/usr/bin/env ipy
import clr
clr.AddReference('WatiN.Core.dll')

# .NET imports
import WatiN.Core as Watin

# Python imports
import sys
sys.path.append('C:\Python26\Lib')
sys.path.append('C:\Python25\Lib')

import optparse
import time
import unittest

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

class _WatinTestResult(unittest._TextTestResult):
    def startTest(self, test):
        for k, v in self.passed.iteritems():
            if not v:
                continue
            setattr(test, k, v)
        unittest._TextTestResult.startTest(self, test)

class WatinTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        self.passalong = kwargs.keys()
        self.__dict__.update(kwargs)
        if self.browser:
            self.browser = self.browser == 'ie' and Watin.IE or Watin.FireFox
        
        super_kwargs = dict([(k, v) for k, v in kwargs.iteritems() if v and k in ('stream', 'descriptions', 'verbosity',)])
        unittest.TextTestRunner.__init__(self, *args, **super_kwargs)

    def _makeResult(self):
        rc = _WatinTestResult(self.stream, self.descriptions, self.verbosity)
        rc.passed = {}
        for key in self.passalong:
            rc.passed[key] = getattr(self, key)
        return rc

def main(options=None):
    op = options or optparse.OptionParser()
    op.add_option('-b', '--browser', dest='browser', default='ie', 
        help='Specify the browser to use [ie/firefox]')
    op.add_option('-u', '--url', dest='url', help='Specify the URL to load in the browser')
    op.add_option('-v', '--verbose', dest='verbose', action='store_true')
    op.add_option('-q', '--quiet', dest='quiet', action='store_true')

    # Blacklist of members of optparse.Values to ignore
    blacklist = dir(optparse.Values)

    opts, args = op.parse_args()
    kwargs = dict([(k, getattr(opts, k)) for k in dir(opts) if not k in blacklist])
    kwargs.pop('quiet')
    kwargs.pop('verbose')

    kwargs['verbosity'] = 1
    if opts.quiet:
        kwargs['verbosity'] = 0
    if opts.verbose:
        kwargs['verbosity'] = 2

    tests = unittest.findTestCases(sys.modules['__main__'])
    runner = WatinTestRunner(**kwargs)
    runner.run(tests)

if __name__ == '__main__':
    main()


#!/usr/bin/env ipy
import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('WatiN.Core.dll')

# .NET imports
from System.Windows import Forms
from System import Drawing
import WatiN.Core as Watin

# Python imports
import sys
sys.path.append('C:\Python26\Lib')
sys.path.append('C:\Python25\Lib')

import optparse
import time
import unittest

def captureScreenshot(filename):
    format = Drawing.Imaging.ImageFormat.Gif
    bounds = Forms.Screen.GetBounds(Drawing.Point.Empty)
    with Drawing.Bitmap(bounds.Width, bounds.Height) as bitmap:
        with Drawing.Graphics.FromImage(bitmap) as gr:
            gr.CopyFromScreen(Drawing.Point.Empty, Drawing.Point.Empty, bounds.Size)
        bitmap.Save(filename, format)

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

global recorder_count

def record(**kwargs):
    file_prefix = kwargs.pop('prefix')
    def _record(method):
        def _record_tracer(frame, event, arg):
            global recorder_count
            #print event, frame.f_code.co_name, frame.f_lineno, "->", arg
            if event == 'line' and frame.f_code.co_name == method.func_name:
                # take picture!
                captureScreenshot('%s_%d.gif' % (file_prefix, recorder_count))
                recorder_count += 1

        def derived_f(obj, *args, **kw):
            global recorder_count
            recorder_count = 0
            try:
                sys.settrace(_record_tracer)
                return method(obj, *args, **kw)
            finally:
                captureScreenshot('%s_%d.gif' % (file_prefix, recorder_count))
                recorder_count = 0
                sys.settrace(None)
        return derived_f
    return _record

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
    rc = runner.run(tests)
    if not rc.wasSuccessful():
        sys.exit(1)

if __name__ == '__main__':
    main()


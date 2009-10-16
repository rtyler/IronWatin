#!/usr/bin/env ipy
import clr
clr.AddReference('WatiN.Core.dll')

# .NET imports
import WatiN.Core as Watin

import IronWatin

from optparse import OptionParser


class FooTest(IronWatin.BrowserTest):
    url = 'http://yahoo.com'

    @IronWatin.record(prefix='foo_test')
    def runTest(self):
        self.browser.Element(Watin.Find.ByName('p')).WaitUntilExists()
        self.browser.Element(Watin.Find.ByName('p')).Click()
        self.browser.TextField(Watin.Find.ByName('p')).TypeText('IronWatin FTW')


if __name__ == '__main__':
    op = OptionParser()
    op.add_option('--email', dest='email')
    IronWatin.main(options=op)

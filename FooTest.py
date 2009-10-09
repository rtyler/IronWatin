#!/usr/bin/env ipy
import clr
clr.AddReference('WatiN.Core.dll')

# .NET imports
import WatiN.Core as Watin

import IronWatin

from optparse import OptionParser


class FooTest(IronWatin.BrowserTest):
	url = 'http://yahoo.com'
	def runTest(self):
		print ('self', self.__dict__)


if __name__ == '__main__':
	op = OptionParser()
	op.add_option('--email', dest='email')
	IronWatin.main(options=op)

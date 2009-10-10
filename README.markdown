IronWatin
==========

The basic notion behind IronWatin is to use the flexibilty 
provided by [IronPython](http://ironpython.codeplex.com/) 
and the testing power that [WatiN](http://watin.sourceforge.net/) 
provides for integration testing on Windows (not yet tested on Mac OS X or 
Linux via [Mono](http://mono-project.com)).

Status
-------
Currently IronWatin is quite basic in its implementation, providing a 
basic `BrowserTest` class which subclasses from the `unittest.TestCase` 
class provided by the standard [unittest](http://docs.python.org/library/unittest.html)
Python module. 

Usage
------
IronWatin is intended on being used from a single-runner perspective, i.e.:

	#!/usr/bin/env ipy

	# The import of IronWatin will add a reference to WatiN.Core.dll
	# and update `sys.path` to include C:\Python25\Lib and C:\Python26\Lib
	# so you can import from the Python standard library
	import IronWatin

	import WatiN.Core as Watin

	class MyTest(IronWatin.BrowserTest):
		url = 'http://www.github.com'

		def runTest(self):
			# Run some Watin commands

	if __name__ == '__main__':
		IronWatin.main()


You can also add your own custom command-line parameters which will be
added to every instance of your test cases, i.e.:

	#!/usr/bin/env ipy

	# The import of IronWatin will add a reference to WatiN.Core.dll
	# and update `sys.path` to include C:\Python25\Lib and C:\Python26\Lib
	# so you can import from the Python standard library
	import IronWatin

	import WatiN.Core as Watin
	import optparse

	class OptionTest(IronWatin.BrowserTest):
		url = 'http://www.github.com'

		def runTest(self):
			# Run some Watin commands
			assert self.testval

	if __name__ == '__main__':
		opts = optparse.OptionParser()
		opts.add_option('--testval', dest='testval', help='Specify a value')
		IronWatin.main(options=opts)




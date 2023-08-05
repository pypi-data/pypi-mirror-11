from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()



setup(
	name="gtrends",
	version = "0.1",
	py_modules = ["gtrends", "_login"],
	description = "Automated Google Trends downloader.",
	author = "Eric Salina",
	author_email = "ecsalina@gmail.com",
	url = "https://github.com/ecsalina/gtrends",
	license = "MIT",
	long_description = long_description,

	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Utilities",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7"
	]
)
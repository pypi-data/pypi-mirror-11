curmit
======

[![Build Status](http://img.shields.io/travis/jacebrowning/curmit/master.svg)](https://travis-ci.org/jacebrowning/curmit)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/curmit/master.svg)](https://coveralls.io/r/jacebrowning/curmit)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/curmit.svg)](https://scrutinizer-ci.com/g/jacebrowning/curmit/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/curmit.svg)](https://pypi.python.org/pypi/curmit)
[![PyPI Downloads](http://img.shields.io/pypi/dm/curmit.svg)](https://pypi.python.org/pypi/curmit)

Grabs text from a URL and commits it.

Some possible use cases:

 * collaborate on Markdown/LaTeX using Google Drive
 * incorporate and link to online code snippets 
 * archive the history of a webpage

Requirements
------------

* Python 3.3+
* Git

Installation
------------

curmit can be installed with pip:

```
$ pip3 install curmit
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/curmit.git
$ cd curmit
$ python3 setup.py install
```

Setup
-----

1. Create a new text file
2. Add the following somewhere in the first few lines:

        curmit: <http://example.com>

    with your desired URL. An example using a Google Docs can be found [here](https://github.com/jacebrowning/curmit/blob/master/docs/sample.md).

Usage
-----

To update every flagged file with the current URL text, commit, and push:

```
$ curmit
```

**That's it!**

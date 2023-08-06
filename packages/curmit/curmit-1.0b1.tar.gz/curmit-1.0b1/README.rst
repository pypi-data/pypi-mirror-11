curmit
======

| |Build Status|
| |Coverage Status|
| |Scrutinizer Code Quality|
| |PyPI Version|
| |PyPI Downloads|

Grabs text from a URL and commits it.

Some possible use cases:

-  collaborate on Markdown/LaTeX using Google Drive
-  incorporate and link to online code snippets
-  archive the history of a webpage

Requirements
------------

-  Python 3.3+
-  Git

Installation
------------

curmit can be installed with pip:

::

    $ pip3 install curmit

or directly from the source code:

::

    $ git clone https://github.com/jacebrowning/curmit.git
    $ cd curmit
    $ python3 setup.py install

Setup
-----

#. Create a new text file
#. Add the following somewhere in the first few lines:

   ::

       curmit: <http://example.com>

   with your desired URL. An example using a Google Docs can be found
   `here <https://github.com/jacebrowning/curmit/blob/master/docs/sample.md>`__.

Usage
-----

To update every flagged file with the current URL text, commit, and
push:

::

    $ curmit

**That's it!**

.. |Build Status| image:: http://img.shields.io/travis/jacebrowning/curmit/master.svg
   :target: https://travis-ci.org/jacebrowning/curmit
.. |Coverage Status| image:: http://img.shields.io/coveralls/jacebrowning/curmit/master.svg
   :target: https://coveralls.io/r/jacebrowning/curmit
.. |Scrutinizer Code Quality| image:: http://img.shields.io/scrutinizer/g/jacebrowning/curmit.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/curmit/?branch=master
.. |PyPI Version| image:: http://img.shields.io/pypi/v/curmit.svg
   :target: https://pypi.python.org/pypi/curmit
.. |PyPI Downloads| image:: http://img.shields.io/pypi/dm/curmit.svg
   :target: https://pypi.python.org/pypi/curmit

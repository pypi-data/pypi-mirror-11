Digs
====

Making easier the text crawling tasks over websites with depth levels.

|PyPI Package latest release| |Code Quality Status| |PyPI Package
monthly downloads| |GitHub issues for digs|

Installation
------------

::

    pip install digs

or

::

    pip install --upgrade digs

Usage
-----

Common use will be extract the text from a website, the following call
from terminal is the way to do that:

::

    digs http://thewebsite.com

Also, you can add the option --depth=LEVEL to perform over the root
domain (website) a crawling with the specific depth:

::

    digs http://thewebsite.com --depth=3

Be careful, with high levels, the tree asociated to those crawlings
grows exponentially in size.

And last but not the least, you can turn on a graphical interface (if
you have installed PySide) with the following call from terminals:

::

    digs -i

It will be look something like this:

|GUI|

About requirements
------------------

Look at requirements in the file: :

::

    requirements.txt

digs was written by `Jonathan S. Prieto C. <prieto.jona@gmail.com>`__.

|Bitdeli badge|

.. |PyPI Package latest release| image:: http://img.shields.io/pypi/v/digs.png?style=flat
   :target: https://pypi.python.org/pypi/digs
.. |Code Quality Status| image:: https://landscape.io/github/d555/digs/master/landscape.svg?style=flat
   :target: https://landscape.io/github/d555/digs/master
.. |PyPI Package monthly downloads| image:: http://img.shields.io/pypi/dm/digs.png?style=flat
   :target: https://pypi.python.org/pypi/digs
.. |GitHub issues for digs| image:: https://img.shields.io/github/issues/d555/digs.svg?style=flat-square
   :target: https://github.com/d555/digs/issues
.. |GUI| image:: https://raw.githubusercontent.com/d555/digs/master/gui.png
   :target: https://pypi.python.org/pypi/digs
.. |Bitdeli badge| image:: https://d2weczhvl823v0.cloudfront.net/d555/digs/trend.png
   :target: https://bitdeli.com/free

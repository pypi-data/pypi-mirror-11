|pypi| |pypi| |GitHub license| |travis| |coveralls|

erajp: Convert datetime to Japanese era
=======================================

Requirements
------------

-  Python 2.7+
-  Python 3.2+

Installation
------------

Install erajp via PyPI:

::

    pip install erajp

How to use
----------

.. code:: python

    >>> strjpftime()
     'H27.08.05' # now
    >>> strjpftime(datetime.datetime(1989, 1, 8)) 
     'H1.01.08'
    >>> strjpftime(datetime.datetime(1989, 1, 8), u"%O%E年")
     '平成元年'

New available date format
~~~~~~~~~~~~~~~~~~~~~~~~~

-  %o : alpabet era
-  %O : Chinese charactor era
-  %E : era year

Main Project Website.
---------------------

https://github.com/recruit-mtl/erajp

License
-------

MIT License

.. |pypi| image:: https://img.shields.io/pypi/dm/erajp.svg
   :target: https://pypi.python.org/pypi/erajp
.. |pypi| image:: https://img.shields.io/pypi/v/erajp.svg
   :target: https://pypi.python.org/pypi/erajp
.. |GitHub license| image:: https://img.shields.io/github/license/recruit-mtl/erajp.svg
   :target: https://github.com/recruit-mtl/erajp
.. |travis| image:: https://img.shields.io/travis/recruit-mtl/erajp.svg
   :target: https://travis-ci.org/recruit-mtl/erajp
.. |coveralls| image:: https://img.shields.io/coveralls/recruit-mtl/erajp.svg
   :target: https://coveralls.io/github/recruit-mtl/erajp

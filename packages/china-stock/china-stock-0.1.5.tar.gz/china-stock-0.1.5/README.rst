china-stock
===========

.. image:: https://travis-ci.org/fuermosi777/china-stock.svg?branch=master

Author: `Hao Liu <http://liuhao.im>`_

~~~~~~~
Install
~~~~~~~

::

	$ pip install china-stock

~~~
Use
~~~

Import china-stock module:

::
    
    >>> import chinastock as cs

Get stock prices information on nearest trading day:

::

	>>> cs.get_stock_today(code='000001', exchange='SZ')

Get historical stock close prices:

::

    >>> cs.get_stock_history(code='000001', exchange='SZ')

Get stock's adjusted close prices, open, high, low, volume, and change:

::

    >>> cs.get_stock_history_adj(code='000001', exchange='SZ')

~~~~~~
Update
~~~~~~

07/14/2015:
    * Add :code:`get_stock_history` and :code:`get_stock_history_adj` methods
    * :code:`get_stock_today` method return strings, not :code:`datetime`
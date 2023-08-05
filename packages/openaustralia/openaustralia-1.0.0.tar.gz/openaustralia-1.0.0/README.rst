OpenAustralia API Python Client
===============================

.. image:: https://drone.io/bitbucket.org/otherchirps/openaustralia-api-py/status.png
  :target: https://drone.io/bitbucket.org/otherchirps/openaustralia-api-py/latest

This is a python wrapper for the `OpenAustralia API <http://www.openaustralia.org.au/api>`_.

NOTE: This isn't officially affiliated with the `OpenAustralia <http://www.openaustralia.org.au>`_ project. 
It's just something I'm playing around with. Suggestions / contributions towards making this more useful are welcome.

Documentation
-------------

You can find the package documentation `here <https://pythonhosted.org/openaustralia>`_.

Installation
------------

From source
~~~~~~~~~~~

``python setup.py install``

pip
~~~

``pip install openaustralia``

Usage
-----

.. code-block:: python

   from openaustralia import OpenAustralia
   
   oa = OpenAustralia("YOUR KEY")
   search = oa.get_hansard("barnacles")
   search['rows'].pop(0)

Source code
-----------

You can get the code here:

https://bitbucket.org/otherchirps/openaustralia-api-py


Testing
-------

`tox <https://pypi.python.org/pypi/tox>`_ is being used to run the tests across
python 2.7 & 3.x. 

To bootstrap your test environment, the easiest way is you 
use the `pip <https://pip.pypa.io/en/latest/installing.htm>`_ requirements file::

    pip install -r requirements.txt

Then you can simply run::

    tox



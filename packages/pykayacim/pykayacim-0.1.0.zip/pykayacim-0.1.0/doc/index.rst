.. PyKayacIM documentation master file, created by
   sphinx-quickstart on Tue Sep  8 16:55:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyKayacIM's documentation!
=====================================

PyKayacIM is a simple package for sending push notifications via
`im.kayac.com <http://im.kayac.com/en/>`_
(`Japanese <http://im.kayac.com/ja/>`_) to your iPhone or Jabbler account.

.. code-block:: python

    >>> import pykayacim.api
    >>> api = pykayacim.api.KayacIMAPI(
            username=u"username", method=u"secret", key=u"secret_key")
    >>> api.send(u"Hello!")

.. toctree::
   :maxdepth: 2
   
   prerequisites
   simpleusage
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


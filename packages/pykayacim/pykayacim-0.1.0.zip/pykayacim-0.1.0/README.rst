PyKayacIM is a simple package for sending push notifications via
`im.kayac.com <http://im.kayac.com/en/>`_
(`Japanese <http://im.kayac.com/ja/>`_) to your iPhone or Jabbler account.

.. code-block:: python

    >>> import pykayacim.api
    >>> api = pykayacim.api.KayacIMAPI(
            username=u"username", method=u"secret", key=u"secret_key")
    >>> api.send(u"Hello!")

Features
========

* Pure-Python package.
* Python 2/3 compatible (thanks to
  `Python-Future <http://python-future.org/>`_ package).
* Includes a simple command-line tool.
* Supports non-English message.


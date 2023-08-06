Simple Usage
============

Try PyKayacIM on the Python interactive interpereter
----------------------------------------------------

To send a push notification using PyKayacIM, just follow these three steps:

#. Import the module :py:mod:`pykayacim.api` , which is the core module of
   PyKayacIM.
#. Intialize an instance of :py:class:`pykayacim.api.KayacIMAPI` by providing
   your user credentials.
#. Invoke :py:meth:`pykayacim.api.KayacIMAPI.send` to send a notification.

.. code-block:: python

   # Step 1
   import pykayacim.api # Import the core module.
   
   # Step 2
   # Read the rest of this document for details about the parameters.
   api = pykayacim.api.KayacIMAPI( # Initialize an instance.
       username=u"yourusername", # The username of your account.
       method=u"secret", # Authorize using the secret key cryptosystem.
       key=u"yoursecretkey") # Your secret key for authorization.
    
   # Step 3
   api.send( # Send a notification.
       message=u"Hello. こんにちは。" # The message.
       handler=u"mailto:example@example.com") # The URI scheme (optional).

Use the command-line tool of PyKayacIM
--------------------------------------

PyKayacIM has a command-line tool named ``ezkayacim``. This tool will be
installed into the directory ``Scripts``. For detailed information
execute ``ezkayacim --help``.

.. code-block:: none
   
   ezkayacim none -s mailto:example@example.com yourusername "Your message"
   ezkayacim password -s http://example.com yourusername メッセージ yourpassword
   ezkayacim secret yourusername message yourkey


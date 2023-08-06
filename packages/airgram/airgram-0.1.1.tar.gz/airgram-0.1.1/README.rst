##############
python-airgram
##############

A python wrapper for making calls to the `Airgram API <http://www.airgramapp.com/api>`_, which enables you to send push notifications to your mobile devices.

Since it is a very shallow wrapper, you can refer to the `official api reference <http://www.airgramapp.com/docs>`_ for details on the functions.

Examples
========
At the time of writing (2015-08-20) airgram is using wrong certificates (`see <https://api.airgramapp.com/1/>`_), which are intended for herokuapp.com. Because of this cert verification needs to be turned off.

Using as a guest
----------------
.. code-block:: python

    from airgram import Airgram
    
    ag = Airgram(verify_certs=False)
    
    # Send a message to a user
    ag.send_as_guest("your@email.com", "Test message from Airgram API", "http://example.com")


Using with an authenticated airgram service
-------------------------------------------
.. code-block:: python

    from airgram import Airgram
    
    ag = Airgram(key="MY_SERVICE_KEY", secret="MY_SERVICE_SECRET", verify_certs=False)
    
    # Subscribe an email to the service
    ag.subscribe("your@email.com")
    
    # Send a message to a subscriber
    ag.send("your@email.com", "Hello, how are you?")
    
    # Send a message to ALL subscribers
    ag.broadcast("Airgram for python is awesome", url="https://github.com/the01/python-airgram")

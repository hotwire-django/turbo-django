Templates
==========

Templates subscribe to streams using the ``turbo_subscribe`` template tag.  Import this tag by calling ``{% load turbo_streams %}``.  Pass a stream name as a string, or pass a Django instance to listen to messages sent to a particular object.  This tag can be called anywhere on the page and can be called multiple times if desired.

.. code-block:: html
    :caption: broadcast_example.html

    <!-- Load the template tag `turbo_subscribe` -->
    {% load turbo_streams %}

    <!-- Listen to the following channels -->
    {% turbo_subscribe 'broadcast_name' %}
    {% turbo_subscribe room %}

    <!-- or listen to a list of streams  -->
    {% turbo_subscribe 'broadcast_name' room %}

    <!-- The page is now subscribed to the `room` object and the "broadcast_name" channels. -->


One can now send html blocks to the subscribed page using the following:

.. code-block:: python

    from turbo import Turbo

    room = Room.objects.first()

    # Send to an instance channel
    Turbo(room).render(
        "new_message.html", {'message': 'New message'}
    ).append(id='messages_container')

    # Send to a broadcast name
    Turbo('broadcast_name').render(
        "alert.html", {'message': 'Server restart in 1 minute.'}
    ).replace(id='alert_div')



``turbo_subscribe tag``
-----------------------

Tells the page to subscribe to the listed name or instance.

Example usage::

    {% load turbo_streams %} <!-- Place on top of template -->
    {% turbo_subscribe 'broadcasts' %} <!-- Place anywhere in template -->

Stream names can be strings or generated from instances::

    {% turbo_subscribe room %}

Listen to multiple streams by adding additional arguments::

    {% turbo_subscribe 'broadcasts' room %}


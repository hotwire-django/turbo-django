Templates
==========

Templates subscribe to streams using the ``turbo_subscribe`` template tag.  Import this tag by calling ``{% load turbo_streams %}``.  Pass a channel object, name-spaced channel name as a string, or pass a Django instance to listen to messages sent to a particular object.  This tag can be called anywhere on the page and can be called multiple times if desired.

.. code-block:: html
    :caption: broadcast_example.html

    <!-- Load the template tag `turbo_subscribe` -->
    {% load turbo_streams %}

    <!-- Listen to the following channels -->
    {% turbo_subscribe RoomListChannel %}
    {% turbo_subscribe 'chat:RoomListChannel' %}
    {% turbo_subscribe room %}

    <!-- or listen to a list of streams  -->
    {% turbo_subscribe 'chat:RoomListChannel' room %}

    <!-- The page is now subscribed to the `room` instance and the RoomListChannel channels. -->


It is now possible to send and place html to the subscribed page using the following:

.. code-block:: python

    from turbo import Turbo

    # Send to a standard Channel
    RoomListChannel.replace(
        "alert.html",
        {'message': 'Server restart in 1 minute.'},
        id='alert_div'
    )


    # Send to a ModelChannel
    room = Room.objects.first()

    room.channel.append(
        "new_message.html",
        {'message': 'New message'}
        id='messages_container'
    )




``turbo_subscribe tag``
-----------------------

Tells the page to subscribe to the channel or instance.

Example usage::

    {% load turbo_streams %} <!-- Place on top of template -->
    {% turbo_subscribe 'chat:BroadcastChannel' %} <!-- Place anywhere in template -->

Stream names can be strings or generated from instances::

    {% turbo_subscribe room %}

Listen to multiple streams by adding additional arguments::

    {% turbo_subscribe 'chat:BroadcastChannel' room %}


========================================
Part 4 - Pushing data with Turbo Streams
========================================

Turbo Streams
=============

Turbo Streams allow HTML to be pushed to the client page without a request from the client.  The client needs to subscribe to a stream and this is done with the :doc:`turbo_subscribe tag </topics/templates>`.

Add the following:

.. code-block:: html
    :caption: templates/chat/room_detail.html

    {% load turbo_streams %} <!-- Place on top of template -->
    {% turbo_subscribe room %} <!-- Place anywhere in template -->

* ``load turbo_streams`` allows use of the ``turbo_subscribe`` tag.
* ``turbo_subscribe`` subscribes to the Room instance stream.

Since we want message lines to be dynamic, every message line must now be turned into a component.  Replace the message loop with:


.. code-block:: html
    :caption: templates/chat/room_detail.html

    {% for message in room.messages.all %}
        {% include "chat/components/message.html" with message=message only %}
    {% endfor %}

.. code-block:: html
    :caption: templates/chat/components/message.html

    <li>{{message.created_at}}: {{message.text}}</li>


The model now needs to send a rendered message to stream subscribers on each save.  Turbo-django makes this a breeze.

Create a new file in the chat application called ``streams.py``


.. code-block:: python
    :caption: chat/streams.py

    import turbo
    from .models import Message

    class RoomStream(turbo.ModelStream):
        class Meta:
            model = Room


    class MessageStream(turbo.ModelStream):

        class Meta:
            model = Message

        def on_save(self, message, created, *args, **kwargs):
            if created:
                message.room.stream.append(
                    "chat/components/message.html", {"message": message}, id="messages"
                )


The file ``streams.py`` is automatically detected by the Turbo Django library and is the recommended location for all stream-related code.  In this example, a ``ModelStream`` is created, which is a type of stream attached to a model instance.  The model to tie the stream to is defined in the Meta class.  This attaches a ``.stream`` TurboStream attribute to the instance.  Now the instance can be subscribed to, and have data streamed to those subscribers.

In this example, the chat room is what is being subscribed to, but the message is the model being saved - so we create both ModelStreams, and in the Message's ``on_save`` signal, we call on the parent room's stream to append a new message component.

Run this code and see it work in the browser.  Now open up a new window and see how the pages update each other.

Congratulations!  You have created a basic chat application.  In the  :doc:`next tutorial </tutorial/part_5>`, we'll add even more functionality.

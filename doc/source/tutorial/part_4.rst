=====================================
Part 4 - Pushing data with Broadcasts
=====================================

Broadcasts
==========

Broadcasts allow HTML to be sent to the client page without a request from the client.  The client does need to subscribe to broadcasts and this is done with the :doc:`turbo_subscribe tag </topics/templates>`.

Add the following:

.. code-block:: html
    :caption: templates/chat/room_detail.html

    {% load turbo_streams %} <!-- Place on top of template -->
    {% turbo_subscribe room %} <!-- Place anywhere in template -->

* ``load turbo_streams`` allows use of the ``turbo_subscribe`` tag.
* ``turbo_subscribe`` subscribes to the room instance channel name.  Channel names can be generated from instances or custom strings.

We need to each message line into a component.  Replace the message loop with:


.. code-block:: html
    :caption: templates/chat/room_detail.html

    {% for message in room.messages.all %}
        {% include "chat/components/message.html" with message=message only %}
    {% endfor %}

.. code-block:: html
    :caption: templates/chat/components/message.html

    <li>{{message.created_at}}: {{message.text}}</li>


The model now needs to send a rendered message to subscribers on each save.  Turbo-django makes this a breeze.new

First - add ``TurboMixin`` to your models.

.. code-block:: python
    :caption: chat/models.py

    from turbo.mixins import TurboMixin

    class Room(TurboMixin, models.Model):
        ...

    class Message(TurboMixin, models.Model):
        ...

This adds a convenient ``.turbo`` convenience attribute to your model instances.  We can now use ``instance.turbo`` to broadcast data.

Create ``broadcasts.py`` in the `chat/` directory.

.. code-block:: python
    :caption: chat/broadcasts.py

    from .models import Message, Room

    import turbo

    @turbo.register(Message)
    class MessageBroadcast(turbo.ModelBroadcast):

        def on_save(self, message, created, *args, **kwargs):
            if created:
                message.room.turbo.render(
                    'chat/components/message.html',
                    {'message': message}
                ).append(id='messages')



This file is automatically detected by the Turbo Django library.  The library then registers the `on_save` and `on_delete` methods to the specified model.  In this example, anytime a message is saved, we broadcast a message to the message's room using ``message.room.turbo``.  This returns a `Turbo()` object.  Turbo objects have a render method, similar to Django's render method that returns a ``TurboRender`` object.  That rendered template is then broadcast with ``append()`` and tells all subscribed clients to append the rendered template to the HTML element with the id of `#messages`.

Run this code and see it work in the browser.  Now open up a new window and see how the pages update each other.

Congratulations!  You have created a basic chat application.  In the  :doc:`next tutorial </tutorial/part_5>`, we'll add even more functionality.

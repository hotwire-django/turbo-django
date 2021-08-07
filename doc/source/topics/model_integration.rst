=================
Model Integration
=================

TurboMixin
==========

Adding ``TurboMixin`` to django model classes will assign the result of ``turbo.Turbo(instance)`` to the instance attribute ``.turbo``  This allows for logical broadcasting from the instance itself.

Implementation
--------------

.. code-block:: python

    # models.py
    from django.db import models

    from turbo.mixins import TurboMixin

    class Room(TurboMixin, models.Model):
        name = models.CharField(max_length=255)


Calling
--------------

.. code-block:: python

    room = Room.objects.first()
    room.turbo.render('template.html', {'room': room}).append(id='element_id')

    # is the same as calling...
    from turbo import Turbo
    Turbo(room).render('template.html', {'room': room}).append(id='element_id')


.. admonition:: Primary Key Needed

    You can only broadcast to instances that have a primary key.  A ``ValueError`` is thrown when trying to broadcast to an object that does not have a primary key set.


ModelBroadcast
==============

A common use-case for broadcasts is to send page updates when a model is created, modified, or deleted.  To organize these events in one place, turbo-django uses ``ModelBroadCast``.  When registered to a particular model, these classes will trigger the appropriate method on save and delete.  ``ModelBroadcast`` objects are automatically detected when place in  ``broadcasts.py``.

Sample `broadcasts.py`
----------------------

.. code-block:: python
    :caption: app/broadcasts.py

    from .models import Message, Room

    import turbo

    @turbo.register(Room)
    class RoomBroadcast(turbo.ModelBroadcast):

        def on_save(self, room, created, *args, **kwargs):
            room.turbo.render("chat/room_name.html", {"room": room}).replace(id="update-room")


    @turbo.register(Message)
    class MessageBroadcast(turbo.ModelBroadcast):

        def on_save(self, message, created, *args, **kwargs):
            if created:
                message.room.turbo.render("chat/message.html", {"message": message}).append(id="messages")
            else:
                message.room.turbo.render("chat/message.html", {"message": message}).replace(id=f"message-{message.id}")

        def on_delete(self, message, *args, **kwargs):
            message.room.turbo.remove(id=f"message-{message.id}")

=================
ModelStream
=================


A common reason to stream data is to send page updates when a model is created, modified, or deleted.  To organize these events in one place, Turbo Django uses ``ModelStream``.  These classes will trigger the code to run when a model instance is saved and deleted.  ``ModelStream`` objects are declared and automatically detected in ``streams.py``.

When a ModelStream is registered to a model, the model instance will automatically gain a `.stream` attribute that references the stream.  For this reason, only one model stream can be attached to each model.

.. admonition:: Primary Key Needed

    You can only broadcast to instances that have a primary key.  A ``ValueError`` is thrown when trying to broadcast to an object that does not have a primary key set.


Example
----------------------

The following demonstrates a sample implementation of ModelStreams for a chat application.  In this examples, a user would subscribe to a Room, however, the messages are the items being added and removed.  A stream is created for both models - giving them both `.stream` attributes.  When the message is saved, the message then references it's parent room stream, and either appends or replaces the chat message if it was created or modified.  If the message is deleted, the parent room stream is notified to remove the message block with the provided id.

.. code-block:: python
    :caption: app/streams.py

    from .models import Message, Room

    import turbo

    class RoomStream(turbo.ModelStream):

        class Meta:
            model = Room



    class MessageStream(turbo.ModelStream):

        class Meta:
            model = Message

        def on_save(self, message, created, *args, **kwargs):
            if created:
                message.room.stream.append("chat/message.html", {"message": message}, id="messages")
            else:
                message.room.stream.replace("chat/message.html", {"message": message}, id=f"message-{message.id}")

        def on_delete(self, message, *args, **kwargs):
            message.room.stream.remove(id=f"message-{message.id}")

        def user_passes_test(self, user):
            # if user.can_access_message(self.pk):
            #    return True
            return True

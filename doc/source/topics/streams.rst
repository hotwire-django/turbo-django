=======
Streams
=======

Streams allow data to be sent to a currently loaded page.  Stream classes must be explicitly declared in `streams.py` and should contain all render and positioning logic.  Stream classes are also used to add permissions.


Example
----------------------

.. code-block:: python
    :caption: app/streams.py

    from .models import Message, Room

    import turbo

    class BroadcastStream(turbo.Stream):

        def send_message(self, message):
            # This is a user-defined method that encapsulates render and positioning logic.
            # It would be called from code using BroadcastStream().send_message("test message")
            self.update(text=message, id="broadcast_box")

        def user_passes_test(self, user):
            # user_passes_test is a built-in method that is extended to add permissions to streams.
            return True


.. module:: turbo.Stream


.. method:: append(template=None, context=None, text=None, selector=None, id=None)

    Add the rendered template to the end of the specified HTML element.

.. method:: prepend(template=None, context=None, text=None, selector=None, id=None)

    Add the rendered template to the beginning of the specified HTML element.

.. method:: replace(template=None, context=None, text=None, selector=None, id=None)

    Remove and replace the specified HTML element with the rendered template.

.. method:: update(template=None, context=None, text=None, selector=None, id=None)

    Replace the contents inside the specified HTML element with the rendered template.

.. method:: before(template=None, context=None, text=None, selector=None, id=None)

    Insert the rendered template before the specified HTML element.

.. method:: after(template=None, context=None, text=None, selector=None, id=None)

    Insert the template after the specified HTML element.

.. method:: remove(selector=None, id=None)

    Remove the given HTML element.  The rendered template will not be used.  As no template is used to remove divs, this can also be called directly from the shortcut ``remove_frame()``.  Ex: ``remove_frame(id='div_to_remove')``

.. method:: stream(frame: "TurboRender")

    Send a :doc:`TurboRender </topics/turbo>` object to this stream.

.. method:: stream_raw(raw_text: str)

    Send raw text to this stream.  This will not be prewrapped in a turbo stream tag as it would be in `stream()`

.. method:: user_passes_test(user) -> bool

    Return True if a user has permission to access this stream.  If False, the websocket connection will be rejected.  When creating a stream, extend this method to exclude certain users from resources.



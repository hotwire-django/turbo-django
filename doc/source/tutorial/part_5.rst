=====================================
Part 5 - More Fun with Broadcasts
=====================================

Removing Chat Messages
======================

Let's continue to build on this basic chat application by allowing the user to remove messages. Let's walk through the steps to accomplish this:

* Add links to the `message` component template to remove the message.
* Add a ``message_id`` to each list item so Turbo knows which message to delete.
* Create a view that deletes the message.
* Add an ``on_delete`` method to the ModelStream.  Tell the room subscribers to remove the message using the html id value.


Start by adding a unique id to each ``<li>`` element.  Then add a link to remove that message in the template.

.. code-block:: html
    :caption: templates/chat/components/message.html

    <li id="message-{{message.id}}">
      {{message.created_at}}: {{message.text}} 
      <a href="{% url 'message_delete' message.id %}">[Remove]</a>
    </li>


As this link is outside a turbo-frame, this delete link will replace the contents of the entire page.  To only send a request to the ``message_delete`` url, the links need to be inside a turbo-frame.  Wrap the `<ul>` element in ``room_detail.html`` inside a turbo frame.

.. code-block:: html
    :caption: templates/chat/room_detail.html
    :emphasize-lines: 1,7

    <turbo-frame id="message-list">
        <ul id="messages">
            {% for message in room.messages.all%}
                {% include "chat/components/message.html"  with message=message only %}
            {% endfor %}
        </ul>
    </turbo-frame>



Add the `message_delete` url and view.

.. code-block:: python
    :caption: turbotutorial/urls.py

    urlpatterns = [
       ...
       path("message/<pk:message_id>/delete", views.message_delete, name="message_delete"),
    ]

.. code-block:: python
    :caption: chat/views.py

    from django.http import HttpResponse

    ...

    def message_delete(request, message_id):
        message = get_object_or_404(Message, pk=message_id)
        message.delete()
        return HttpResponse()

And finally, broadcast to clients subscribed to the message's room to remove any item on the page with the unique id specified in the template.

.. code-block:: python
    :caption: chat/broadcasts.py

    class MessageStream(turbo.ModelStream):

        ...

        def on_delete(self, message, *args, **kwargs):
            message.room.stream.remove(id=f"message-{message.id}")


.. note::
   Notice that ``.remove()`` is used without first calling ``.render()``.  Remove only takes away content, so rendering a template is not necessary.


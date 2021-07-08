Broadcasts
^^^^^^^^^^

Broadcasts allow html to be pushed to the user.  First, create a view that takes a broadcast name.

.. code-block:: html
    :caption: broadcast_example.html

    {% turbo_stream_from 'broadcast_name' %}
    <p class="broadcast_box_class" id="broadcast_box">Placeholder for broadcasts</p>


Then create a view that sends the broadcast.  The broadcast is initialized with the broadcast name,
and an action is chosen to determine how the html block is inserted into the page.  Finally `render()` is called, pointing to the template and context to be used to create the html.

.. code-block:: python
    :caption: views.py

    from turbo import Broadcast
    from django.http import HttpResponse
    from datetime import datetime

    def send_broadcast(request):

        context = {"broadcast": f"{datetime.now()}: This is a broadcast and NO MESSAGE"}
        Broadcast('broadcast_name').append(selector=".messages_class").render(
            "chat/broadcast.html", context
        )

        return HttpResponse("Sent a Broadcast")



.. admonition:: API change

    `Broadcast()` objects replaced `turbo.broadcast_stream()` in release 0.1.2.

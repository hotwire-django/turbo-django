===============================
Part 3 - Your First Turbo Frame
===============================

Listen to Websockets
=========================

It's time to start creating a dynamic, interactive application.  Start by getting django to listen to websockets by modying ``asgi.py`` to the following:

.. code-block:: python
    :caption: turbodjango/asgi.py

    import os

    from django.core.asgi import get_asgi_application
    from channels.routing import ProtocolTypeRouter
    from turbo.consumers import TurboStreamsConsumer

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turbodjango.settings')


    application = ProtocolTypeRouter({
      "http": get_asgi_application(),
      "websocket": TurboStreamsConsumer.as_asgi()  # Leave off .as_asgi() if using Channels 2.x
    })



A Component-Based Mindset
=========================

Like many modern javascript-based frameworks, it is helpful to start thinking of the webpage as constructed of components.  This means breaking down templates into sub-templates with one specific function that are used as the building blocks for each page.

With that in mind, let's make a directory for these templates and create our first component - a form to create a message in the chat room.


.. code-block:: html
    :caption: templates/chat/room_detail.html

        <head>
            <meta charset="UTF-8">
            <title>Room Detail</title>
            {% include "turbo/head.html" %} <!-- Add this to load the Turbo javascript library-->
        </head>

        ...
            <!-- Add this to the end of the page-->
            <turbo-frame id="send-message" src="{% url 'message_create' room.id %}"></turbo-frame>
        </body>
        </html>


.. code-block:: html
    :caption: chat/templates/components/send_message.html

    <turbo-frame id="send-message">
         <form method="post" action="{% url 'send_message' room_id %}" data-turbo-frame="messages">
            {% csrf_token %}
            {{ form.as_p }}
            <input type="submit" value="Send">
        </form>
    </turbo-frame>


Introducing the ``turbo-frame`` tag
===================================

**<turbo-frame>** This html  Turbo Frames allow parts of the page to be updated on request.  Each turbo-frame must have a unique id so that new content knows where to position the incoming content.

.. note::
    Be sure to read the `official documentation of Turbo Frames <https://turbo.hotwired.dev/handbook/frames>`_.


Run the code and test.  When text is submitted in the text box, the box is cleared and ready for new entry.  Let's walk through what is happening:

* In `room_detail.html`, the makes a page makes a new request to the url specified in the ``src`` attribute.
* Turbo looks for a turbo-frame with the same id in the response and inserts the content into the parent frame.  The form is now display in the page.
* The user types content into the form and hits submit.
* The framed form is submitted without the page reloading.  The success url returns a new blank form which is instered into the frame.

// The ``get_success_url`` method returns another rendered version of the `message create` form.  This has a ``<turbo-frame id="send-message">`` tag which is then inserted into the tag with the same id on the parent page.


Refreshing the page renders the submitted messages. But for a chat client, we need those messages to appear immediately on this page, and others.  For that, we use  :doc:`broadcasts </tutorial/part_4>`.


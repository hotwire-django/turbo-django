==============================================
Part 2 - Models, Views, and Templates
==============================================

Begin by building out the models, views and templates used in the chat application.  Nothing is this section is Turbo-specific - that will be introduced in  :doc:`the next section </tutorial/part_3>`.

Models
==============

This chat application will be set up with two simple models: ``Rooms`` and ``Messages``.  Start by creating the models with in ``chat/models.py``

.. code-block:: python
    :caption: chat/models.py

    from django.db import models

        class Room(models.Model):
            name = models.CharField(max_length=255)

        class Message(models.Model):

            room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
            text = models.CharField(max_length=255)
            created_at = models.DateTimeField(auto_now_add=True)



Make a migration and migrate, and then create a test room.

.. code-block:: shell

    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py shell


.. code-block:: python

    >>> from chat.models import Room
    >>> Room.objects.create(name="Test Room")
    <Room: Room object (1)>
    >>> exit()


Views and URLs
================================

This tutorial uses generic class-based views to keep the tutorial consise.  Add generic `List`, `Detail`, and `Update` views to ``chat/views.py``, and the urls to access them.  There is nothing turbo-specific in the following section - we'll be adding that next.

.. code-block:: python
    :caption: chat/views.py

    from django.shortcuts import render, reverse, get_object_or_404

    from django.views.generic import CreateView, ListView, DetailView

    from chat.models import Room, Message

    class RoomList(ListView):
        model = Room
        context_object_name = "rooms"


    class RoomDetail(DetailView):
        model = Room
        context_object_name = "room"


    class MessageCreate(CreateView):
        model = Message
        fields = ["text"]
        template_name = "chat/components/create_message.html"

        def get_success_url(self):
            # Redirect to the empty form
            return reverse("send", kwargs={"pk": self.kwargs["pk"]})

        def form_valid(self, form):
            room = get_object_or_404(Room, pk=self.kwargs["pk"])
            form.instance.room = room
            return super().form_valid(form)


.. code-block:: python
    :caption: turbotutorial/urls.py

    from chat import views

    urlpatterns = [
        path("", views.RoomList.as_view(), name="index"),
        path("<slug:pk>/", views.RoomDetail.as_view(), name="room_detail"),
    ]


Templates
=========

Finally, create the templates for the generic views.

.. code-block:: html
    :caption: turbotutorial/chat/templates/room_list.html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Chat Rooms</title>
    </head>
    <body>
        <h1>Room List</h1>
        <ul>
        {% for room in rooms %}
            <li><a href="{% url 'room_detail' room.id %}">{{ room.name }}</a></li>
        {% empty %}
            <li>No Rooms Available</li>
        {% endfor %}
        </ul>
    </body>
    </html>

.. code-block:: html
    :caption: turbotutorial/chat/templates/room_detail.html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Room Detail</title>
    </head>
    <body>

        <a href="{% url 'room_list' %}">Home</a>

        <h1>{{ room.name }}</h1>

        <ul id="messages">
            {% for message in room.messages.all %}
                <li>{{message.created_at}}: {{message.text}}</li>
            {% endfor %}
        </ul>

    </body>
    </html>

.. code-block:: html
    :caption: turbotutorial/chat/templates/room_form.html

    <form method="post" action=".">
       {% csrf_token %}
       {{ form.as_p }}
       <input type="submit" value="Submit">
    </form>

Test in your browser to ensure each of the views correctly load.  You should be able to get to the `Test Room` detail page from the room list.  This application will now display all rooms and messages for each room, but a page refresh is required to see changes.  It is time to spice things up and add  :doc:`some interactivity </tutorial/part_3>` to this basic app.



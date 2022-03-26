==========
Quickstart
==========

Want to see Turbo in action?  Here's a simple broadcast that can be setup in less than a minute.

**The basics:**

* A Turbo Stream class is declared in python.

* A template subscribes to the Turbo Stream.

* A command sends a content block to all subscribed pages and replaces html with the new content.


Example
=============

First, declare the Stream.

.. code-block:: python
    :caption: streams.py

    import turbo


Then, create a template that subscribes to the stream.

.. code-block:: python
    :caption: urls.py

    from django.urls import path
    from django.views.generic import TemplateView

    urlpatterns = [
        path('', TemplateView.as_view(template_name='broadcast_example.html'))
    ]
    class BroadcastStream(turbo.Stream):
        pass


.. code-block:: html
    :caption: broadcast_example.html

    {% load turbo_streams %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        {% include "turbo/head.html" %}
    </head>
    <body>
        {% turbo_subscribe 'broadcast_name' %}

        <p class="broadcast_box_class" id="broadcast_box">Placeholder for broadcast</p>
    </body>
    </html>

.. note::
    Broadcasts can target any HTML element on a page subscribed to its stream. Target elements do not need be wrapped in any ``turbo`` style tag.


Now open ``./manage.py shell``.  Import the Turbo Stream and tell the stream to take the current timestamp and ``update`` the element with id `broadcast_box` on all subscribed pages.

.. code-block:: python

    from quickstart.streams import BroadcastStream
    from datetime import datetime

    BroadcastStream().update(text=f"{datetime.now()}: This is a broadcast.", id="broadcast_box")

With the ``quickstart/`` path open in a browser window, watch as the broadcast pushes messages to the page.

Now change ``.update()`` to ``.append()`` and resend the broadcast a few times. Notice you do not have to reload the page to get this modified behavior.

Excited to learn more?  Be sure to walk through the :doc:`tutorial </tutorial/index>` and read more about what the :doc:`Turbo <turbo>` class can do.

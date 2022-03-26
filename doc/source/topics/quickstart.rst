==========
Quickstart
==========

Want to see Hotwire in action?  Here's a simple broadcast that can be setup in less than a minute.

**The basics:**

* A web page subscribes to a specific broadcast name.

<<<<<<< Updated upstream
* A view sends a rendered template to all subscribed pages telling the page where to position the new content.
=======
* A template subscribes to the Turbo Stream.

* HTML is be pushed to all subscribed pages which replaces the content of specified HTML p tag.
>>>>>>> Stashed changes


Example
=============

<<<<<<< Updated upstream
First, create a view that takes a broadcast name.
=======
First, declare the Stream.

.. code-block:: python
    :caption: streams.py

    import turbo

    class BroadcastStream(turbo.Stream):
        pass

>>>>>>> Stashed changes


.. code-block:: python

    from django.urls import path
    from django.views.generic import TemplateView

    urlpatterns = [
        path('quickstart/', TemplateView.as_view(template_name='broadcast_example.html'))
    ]
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes

.. code-block:: html
    :caption: broadcast_example.html

    {% load turbo_streams %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        {% include "turbo/head.html" %}
    </head>
    <body>
        {% turbo_subscribe 'quickstart:BroadcastStream' %}

        <p class="broadcast_box_class" id="broadcast_box">Placeholder for broadcast</p>
    </body>
    </html>

.. note::
    Broadcasts can target any HTML element on a page subscribed to its stream. Target elements do not need be wrapped in any ``turbo`` style tag.


Now open ``./manage.py shell``.  Create a Turbo object that references the broadcast name.  Tell the object to render a ``TurboRender`` object from the string, and then broadcast a command to ``update`` the inside of the element with id `broadcast_box` on all subscribed pages.

.. code-block:: python

    from turbo import Turbo
    from datetime import datetime

    Turbo('broadcast_name').render_from_string(
        f"{datetime.now()}: This is a broadcast."
    ).update(id="broadcast_box")

With the ``quickstart/`` path open in a browser window, watch as the broadcast pushes messages to the page.

Now change ``.update()`` to ``.append()`` and resend the broadcast a few times. Notice you do not have to reload the page to get this modified behavior.

Excited to learn more?  Be sure to walk through the :doc:`tutorial </tutorial/index>` and read more about what the :doc:`Turbo <turbo>` class can do.

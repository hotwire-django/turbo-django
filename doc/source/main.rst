This package provides helpers for server-side rendering of `Hotwired/Turbo <https://turbo.hotwired.dev/>`_ websocket based Streams.

**Disclaimer**: the Hotwired/Turbo client libraries are, at time of writing, still in Beta. We expect there will be breaking changes until the first stable release. This package, and the Turbo client, should therefore be used with caution in a production environment. The version used in testing is *@hotwired/turbo==7.0.0-beta.2*.

============
Requirements
============

This library is tested for Python 3.6+.

Turbo for Django
================

This repository aims to provide utilities for working with
`Turbo <https://turbo.hotwired.dev>`__
with the Django web framework.

Setup
-----

The first step for setup is to include Turbo in the ``<head>`` for
your templates. Simply put ``{% include 'turbo/head.html' %}`` somewhere
in your head,
which will include the Turbo libraries we need in order to use Turbo
Drive, Frames and Streams in our app.

Turbo Streams
-------------

Currently, the repository contains utilities for working with
`Turbo Streams <https://turbo.hotwired.dev/handbook/streams>`__ over
Websockets, the one part of
Turbo which requires a specific integration with the backend framework
to function. In Django's
case, this means taking advantage of `Django
Channels <https://github.com/django/channels>`__ and ASGI support.

The Django Streams integration is heavily inspired by the helpers and
mixins found in
`turbo-rails <https://github.com/hotwired/turbo-rails>`__. There are a
few steps required to get
the integration working.

Django Channels Setup
~~~~~~~~~~~~~~~~~~~~~

After setting up Channels according to the
`documentation <https://channels.readthedocs.io/en/stable/installation.html>`__,
make sure to modify the top-level ``ProtocolTypeRouter`` to include
the ``TurboStreamsConsumer``:

.. code:: python

    from channels.routing import ProtocolTypeRouter
    from turbo.consumers import TurboStreamsConsumer

    application = ProtocolTypeRouter({
      "http": AsgiHandler(),
      "websocket": TurboStreamsConsumer.as_asgi()  # Leave off .as_asgi() if using Channels 2.x
    })

Model Layer
~~~~~~~~~~~

Throughout these docs we'll be using these two basic models for a chat
app, similar to the
`Hotwire demo video <https://www.youtube.com/watch?v=eKY-QES1XQQ>`__
and the
`Rails demo
app <https://github.com/hotwired/hotwire-rails-demo-chat>`__:

.. code:: python

    # chat/models.py

    from django.db import models
    class Room(models.Model):
        name = models.CharField(max_length=255)


    class Message(models.Model):
        room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
        text = models.TextField()

``turbo-django`` provides a ``BroadcastableMixin`` that enables CRUD
operations from a given model
to be broadcast over websockets. To enable messages to be broadcast
over websocket to users
listening in on a particular room, we add the ``BroadcastableMixin``
and tell ``turbo-django``
that actions on messages should be broadcast to the related ``Room``:

.. code:: python

    class Message(BroadcastableMixin, models.Model):
        broadcast_to = ["room"]
        broadcast_self = False

        room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
        text = models.TextField()

``broadcast_to`` can contain any foreign key field on the model. We
set ``broadcast_self`` to ``False`` since we don't
anticipate listening in to updates on a single message, only on the
associated ``Room``. This is all the set-up on the
model side of things that we'll need!

Template Layer
~~~~~~~~~~~~~~

Subscribing to a stream
^^^^^^^^^^^^^^^^^^^^^^^

Next, we can declare that a given page should subscribe to broadcasts
for a given model instance. Make sure to
``{% load turbo_streams %}`` to get access to the template tag in your
template.

Make sure to pass the model instance (here, it's passed as ``room``)
into the template context. Somewhere in the ``<body>``,
we need to add the template tag ``{% turbo_stream_from room %}``.
That's all we need to do to connect this template, when
rendered on the front-end, to the stream of updates for a given model
instance!

Rendering Streams
^^^^^^^^^^^^^^^^^

Streams need to render HTML of updates on the backend using template
partials to send over to the frontend over the wire.
``turbo-django`` at the moment relies on some conventional names for
templates and IDs:

-  ``app_name/model_name.html`` should contain the template partial for
   rendering the model. The context passed in will
   have the labels ``object`` as well as ``model_name`` refer to the
   instance being rendered. Streams mandates that there's
   one, top-level element wrapping the HTML. You can make sure the
   element's ID is set properly by using the templatetag
   ``{% stream_id object %}`` A consistent element ID is necessary to
   ensure that the Streams CRUD operations, titled
   ``replace``, can predictably find elements on the page.
-  For our example with the ``Message`` model, we should create a
   template called ``chat/message.html``, where the top-level
   HTML element should have the ID ``id={% stream_id message %}``.

-  The page template (the one that contains the ``turbo_stream_from``
   tag) should put the related instances into some
   sort of list, where the ``id`` of the list is the lower-cased plural
   name of the model. This is necessary for Streams's
   insert actions ``append`` and ``prepend``, which need a parent
   container to insert elements into.
-  In our example, there should be a ``div`` or ``ul`` containing
   messages, with the encompassing element's ``id``
   being ``messages``.



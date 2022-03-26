Installation
============

============
Requirements
============

This library is tested for Python 3.8+ and Django 3.1+

============
Installation
============


Turbo Django is available on PyPI - to install it, just run:

.. code-block:: sh

    pip install turbo-django


.. note::

    Both Turbo and Turbo Django are under beta development and the API can change quickly as new features are added and the API is refined.  It would be prudent to pin to a specific version until the first major release.  You can pin with pip using a command like ``pip install turbo-django==0.3.0``.  The latest version can be found `at PyPi <https://pypi.org/project/turbo-django/>`_.

Once that's done, you should add ``turbo`` and ``channels`` to your
``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        ...
        'turbo',
        'channels',
    )

    CHANNEL_LAYERS = {
        # You will need to `pip install channels_redis` and configure a redis instance.
        # Using InMemoryChannelLayer will not work as the stored memory is not shared between threads.
        # See https://channels.readthedocs.io/en/latest/topics/channel_layers.html
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }


.. note::
   Turbo relies on the ``channels`` library to push data to the client (also known as Turbo Streams).  Adding channels may not be needed if using only implementing Turbo Frames to component-ify your app.  For the tutorial, you will need channels installed.


Then, adjust your project's ``asgi.py`` to wrap the Django ASGI application::

    import os

    from django.core.asgi import get_asgi_application
    from channels.routing import ProtocolTypeRouter
    from turbo.consumers import TurboStreamsConsumer

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')


    application = ProtocolTypeRouter({
      "http": get_asgi_application(),
      "websocket": TurboStreamsConsumer.as_asgi()
    })

And finally, set your ``ASGI_APPLICATION`` setting to point to that routing
object as your root application:

.. code-block:: python

    ASGI_APPLICATION = "myproject.asgi.application"

All set! ``turbo`` is now ready to use in your Django app.

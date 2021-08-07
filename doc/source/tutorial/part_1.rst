=============================================
Part 1 - Setup Project
=============================================

In this tutorial we will build a simple chat server. It will consist of two pages:

* The room list - consisting of the list of all available chat rooms.
* The chat room - where anyone can go and post a message.

This tutorial assumes basic knowledge of the Django framework and will use class-based generic views to minimize the amount of code and to focus more on Hotwire.

Create a virtual environment using a tool of your choice and install ``turbo-django``, along with ``django``, and ``channels``.

.. code-block:: shell

    $ pip install django turbo-django channels


Start a django project and create an app called ``chat``

.. code-block:: shell

    $ django-admin startproject turbotutorial
    $ cd turbotutorial/
    $ ./manage.py startapp chat

You should now have a set of directories that looks something like:

.. code-block:: shell

    turbotutorial/
        chat/
            migrations/
            admin.py
            apps.py
            models.py
            tests.py
            views.py
        turbotutorial/
            asgi.py
            settings.py
            urls.py
            wsgi.py


Open ``turbotutorial/settings.py``.

* Add ``turbo``, ``channels``, and ``chat`` to ``INSTALLED_APPS``.
* Change ``WSGI_APPLICATION = 'turbotutorial.wsgi.application'`` to ``ASGI_APPLICATION = 'turbotutorial.asgi.application'``

Your ``settings.py`` file should now look like this.

.. code-block:: python

    ASGI_APPLICATION = 'turbotutorial.asgi.application'


    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'turbo',
        'channels',
        'chat'
    ]

    CHANNEL_LAYERS = {
        "default": {
            # Don't use this backend in production
            # See https://channels.readthedocs.io/en/latest/topics/channel_layers.html
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }



You should now be able to run ``python manage.py runserver``, visit ``http://127.0.0.1:8000/`` and see the standar django startup screen greeting: `The install worked successfully! Congratulations!`. If so, we're ready to :doc:`start coding </tutorial/part_2>`.

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fhotwire-django%2Fturbo-django%2Fbadge%3Fref%3Dmain&style=flat)](https://actions-badge.atrox.dev/hotwire-django/turbo-django/goto?ref=main)
[![Documentation Status](https://readthedocs.org/projects/turbo-django/badge/?version=latest)](https://turbo-django.readthedocs.io/en/latest/?badge=latest)
[![Issues](https://img.shields.io/github/issues/hotwire-django/turbo-django)](https://img.shields.io/github/issues/hotwire-django/turbo-django)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2FDjangoHotwire)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fhotwire-django%2Fturbo-django)

# Turbo for Django


Integrate [Hotwire Turbo](https://turbo.hotwired.dev/) with Django with ease.


## Requirements

- Python 3.8+
- Django 3.1+
- Channels 3.0+ _(Optional for Turbo Frames, but needed for Turbo Stream support)_

## Installation

Turbo Django is available on PyPI - to install it, just run:

    pip install turbo-django

Add `turbo` and `channels` to `INSTALLED_APPS`, and copy the following `CHANNEL_LAYERS` setting:

```python
INSTALLED_APPS = [
    ...
    'turbo',
    'channels'
    ...
]

CHANNEL_LAYERS = {
    "default": {
        # You will need to `pip install channels_redis` and configure a redis instance.
        # Using InMemoryChannelLayer will not work as the memory is not shared between threads.
        # See https://channels.readthedocs.io/en/latest/topics/channel_layers.html
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    }
}

```

And collect static files if the development server is not hosting them:

```sh
./manage.py collectstatic
```

_Note: Both Hotwire and this library are still in beta development and may introduce breaking API changes between releases.  It is advised to pin the library to a specific version during install._

## Quickstart
Want to see Hotwire in action? Here's a simple broadcast that can be setup in less than a minute.

**The basics:**

* A Turbo Stream class is declared in python.

* A template subscribes to the Turbo Stream.

* HTML is be pushed to all subscribed pages which replaces the content of specified HTML p tag.


### Example

First, in a django app called `quickstart`, declare `BroadcastStream` in a file named `streams.py`.

```python
# streams.py

import turbo

class BroadcastStream(turbo.Stream):
    pass

Then, create a template that subscribes to the stream.

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('quickstart/', TemplateView.as_view(template_name='broadcast_example.html'))
]
```

```html
# broadcast_example.html

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
```

Now run ``./manage.py shell``.  Import the Turbo Stream and tell the stream to take the current timestamp and ``update`` the element with id `broadcast_box` on all subscribed pages.

```python
from quickstart.streams import BroadcastStream
from datetime import datetime

BroadcastStream().update(text=f"{datetime.now()}: This is a broadcast.", id="broadcast_box")
```

With the `quickstart/` path open in a browser window, watch as the broadcast pushes messages to the page.

Now change `.update()` to `.append()` and resend the broadcast a few times.  Notice you do not have to reload the page to get this modified behavior.

Excited to learn more?  Be sure to walk through the [tutorial](https://turbo-django.readthedocs.io/en/latest/index.html) and read more about what Turbo can do for you.

## Documentation
Read the [full documentation](https://turbo-django.readthedocs.io/en/latest/index.html) at readthedocs.io.


## Contribute

Discussions about a Django/Hotwire integration are happening on the [Hotwire forum](https://discuss.hotwired.dev/t/django-backend-support-for-hotwire/1570). And on Slack, which you can join by [clicking here!](https://join.slack.com/t/pragmaticmindsgruppe/shared_invite/zt-kl0e0plt-uXGQ1PUt5yRohLNYcVvhhQ)

As this new magic is discovered, you can expect to see a few repositories with experiments and demos appear in [@hotwire-django](https://github.com/hotwire-django). If you too are experimenting, we encourage you to ask for write access to the GitHub organization and to publish your work in a @hotwire-django repository.


## License

Turbo-Django is released under the [MIT License](https://opensource.org/licenses/MIT) to keep compatibility with the Hotwire project.

If you submit a pull request. Remember to add yourself to `CONTRIBUTORS.md`!

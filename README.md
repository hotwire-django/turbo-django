# Turbo for Django

This repository aims to help you integrate [Hotwire Turbo](https://turbo.hotwire.dev/) with Django. Inspiration might be taken from [@hotwired/turbo-rails](https://github.com/hotwired/turbo-rails).
Documentation can be found [here](documentation.md) for the current integration.

Discussions about a Django/Hotwire integration are happening on the [Hotwire forum](https://discuss.hotwire.dev/t/django-backend-support-for-hotwire/1570). And on Slack, which you can join by [clicking here!](https://join.slack.com/t/pragmaticmindsgruppe/shared_invite/zt-kl0e0plt-uXGQ1PUt5yRohLNYcVvhhQ)

## Experiments

As we are several to experiment on the integration, I suggest we all dump our code in a sub-directory of `experiments/` so we can all benefit from the ideas of others. Improvements and utilities can then be generalized out into the `turbo` package at the top-level.

## Turbo
The `turbo` directory contains the package with helpers, templatetags and utilities for integrating Turbo tightly into Django. Currently, it contains a `Broadcastable` mixin and a Django Channels websocket consumer to allow for realtime updates with Turbo Streams.


## License

Turbo-Django is released under the [MIT License](https://opensource.org/licenses/MIT) to keep compatibility with the Hotwire project.

If you submit a pull request. Remember to add yourself to `CONTRIBUTORS.md`!

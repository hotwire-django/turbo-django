_Note_: This is not ready for production. APIs likely to change dramatically. Please drop by our [Slack channel](https://join.slack.com/t/pragmaticmindsgruppe/shared_invite/zt-kl0e0plt-uXGQ1PUt5yRohLNYcVvhhQ) to discuss!

# Turbo for Django

## Requirements

- Python 3.6+
- Django 3.1+
- Channels 3.0+ (Optional for Turbo Stream support)

This repository aims to help you integrate [Hotwire Turbo](https://turbo.hotwire.dev/) with Django. Inspiration taken from [@hotwired/turbo-rails](https://github.com/hotwired/turbo-rails).
Documentation can be found [here](documentation.md) for the current integration.

Discussions about a Django/Hotwire integration are happening on the [Hotwire forum](https://discuss.hotwire.dev/t/django-backend-support-for-hotwire/1570). And on Slack, which you can join by [clicking here!](https://join.slack.com/t/pragmaticmindsgruppe/shared_invite/zt-kl0e0plt-uXGQ1PUt5yRohLNYcVvhhQ)

As we discover this new magic, you can expect to see a few repositories with experiments and demos appear in [@hotwire-django](https://github.com/hotwire-django). If you too are experimenting, we encourage you to ask a write access to the GitHub organization and to publish your work in a @hotwire-django repository.

We expect to gain knowledge and experience with Hotwire over time and will try to extract useful code from the demos and package it in self contained "pip-installable" packages: [turbo-django](https://github.com/hotwire-django/turbo-django) and [stimulus-django](https://github.com/hotwire-django/stimulus-django).

As we are several to experiment on the integration, I suggest we all dump our code in a sub-directory of `experiments/` so we can all benefit from the ideas of others. Improvements and utilities can then be generalized out into the `turbo` package at the top-level.

## Structure
The `turbo` directory contains the package with helpers, templatetags and utilities for integrating Turbo tightly into Django. Currently, it contains a `Broadcastable` mixin and a Django Channels websocket consumer to allow for realtime updates with Turbo Streams.

## License

Turbo-Django is released under the [MIT License](https://opensource.org/licenses/MIT) to keep compatibility with the Hotwire project.

If you submit a pull request. Remember to add yourself to `CONTRIBUTORS.md`!

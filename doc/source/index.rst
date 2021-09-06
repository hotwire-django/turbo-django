Turbo Django
============

Turbo Django is a project that integrates the `Hotwire Turbo framework <https://turbo.hotwired.dev/>`_ with `Django <https://www.djangoproject.com/>`_, allowing for rendered page updates to be delivered over websockets. By keeping template rendering in Django, dynamic and interactive web pages can be written without any serialization frameworks or JavaScript, dramatically simplifying development.

.. warning::
   Both Turbo and this library are under development.  Be sure to pin requirements to avoid issues with API changes.


Topics
------

.. toctree::
   :maxdepth: 2

   installation
   tutorial/index
   topics/quickstart.rst
   topics/turbo.rst
   topics/model_integration.rst
   topics/templates.rst


Reference
---------

.. toctree::
   :maxdepth: 1

   ./autoapi/index.rst
   GitHub Repo <https://github.com/hotwire-django/turbo-django>

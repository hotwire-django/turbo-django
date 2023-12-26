.. warning::
   This library is unmaintained. Integrating Hotwire and Django is so easy
   that you are probably better served by writing a little bit of Python in your code
   than using a full blown library that adds another level of abstraction.
   It also seems that the Django community is leaning more towards HTMX than Hotwire
   so you might want to look over there if you want more "support"
   (but we still think that Hotwire is very well suited to be used with Django)



Turbo Django
============

Turbo Django is a project that integrates the `Hotwire Turbo framework <https://turbo.hotwired.dev/>`_ with `Django <https://www.djangoproject.com/>`_, allowing for rendered page updates to be delivered live, over the wire. By keeping template rendering in Django, dynamic and interactive web pages can be written without any serialization frameworks or JavaScript, dramatically simplifying development.

Topics
------

.. toctree::
   :maxdepth: 2

   installation
   topics/quickstart.rst
   tutorial/index
   topics/turbo.rst
   topics/streams.rst
   topics/model_stream.rst
   topics/components.rst
   topics/templates.rst


Reference
---------

.. toctree::
   :maxdepth: 1

   GitHub Repo <https://github.com/hotwire-django/turbo-django>

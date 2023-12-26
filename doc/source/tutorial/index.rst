.. warning::
   This library is unmaintained. Integrating Hotwire and Django is so easy
   that you are probably better served by writing a little bit of Python in your code
   than using a full blown library that adds another level of abstraction.
   It also seems that the Django community is leaning more towards HTMX than Hotwire
   so you might want to look over there if you want more "support"
   (but we still think that Hotwire is very well suited to be used with Django)


Unmaintained//Tutorial
========

Turbo-Django allows you to easily integrate the Hotwire Turbo framework into your
Django site. This will allow clients to receive blocks of html sent from your web server
without using HTTP long-polling or other expensive techniques.  This makes for
dynamic interactive webpages, without all the mucking about with serializers and JavaScript.

In this tutorial we will build a simple chat server, where you can join an
online room, post messages to the room, and have others in the same room see
those messages immediately.

.. toctree::
   :maxdepth: 1

   part_1
   part_2
   part_3
   part_4
   part_5

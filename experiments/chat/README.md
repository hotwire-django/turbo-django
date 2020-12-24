# Django Hotwire Demo

This repository contains a demonstration of [Hotwire](https://hotwire.dev), specifically the three components of
[Turbo](https://turbo.hotwire.dev) to build a realtime chat app in Django with only server-side custom code. It makes use
of Django Channels for websocket support.

To run this demo, after cloning the repository:
1. `pipenv install`
2. `pipenv shell`
3. `./manage.py migrate`
4. `./manage.py createsuperuser`
5. `./manage.py runserver`
6. Log into `localhost:8000/admin` and create a `Room`
7. Go to `localhost:8000`, select your room, and start chatting! Open as many windows as you'd like.

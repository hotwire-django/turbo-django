# Django Hotwire Demo

This repository contains a demonstration of [Hotwire](https://hotwire.dev), specifically the three components of
[Turbo](https://turbo.hotwire.dev) to build a realtime chat app in Django with only server-side custom code. It makes use
of Django Channels for websocket support.

To run this demo, after cloning the repository:

```bash
cd experiments/chat
virtualenv -p python 3 ve
souce ve/bin/activate
pip install -e ../../

./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Log into `http://localhost:8000/admin` and create a `Room`
Go to `http://localhost:8000`, select your room, and start chatting! Open as many windows as you'd like.

# Django Hotwire Demo

This repository contains a demonstration of [Hotwire](https://hotwire.dev), specifically the three components of
[Turbo](https://turbo.hotwire.dev) to build a realtime chat app in Django with only server-side custom code. It makes use
of Django Channels for websocket support.

To run this demo, after cloning the repository:

```bash
cd experiments/chat
python3 -m venv ve
souce ve/bin/activate
pip install -e ../../
pip install -r requirements.txt

./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata data.json
./manage.py runserver
```

Log into `http://localhost:8000/admin` and create a `Room`
Go to `http://localhost:8000`, select your room, and start chatting! Open as many windows as you'd like.

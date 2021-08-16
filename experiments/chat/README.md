# Django Hotwire Demo

This repository contains a demonstration of [Hotwire](https://hotwired.dev), specifically the three components of
[Turbo](https://turbo.hotwired.dev) to build a realtime chat app in Django with only server-side custom code. It makes use
of Django Channels for websocket support.

To run this demo, after cloning the repository:

```bash
cd experiments/chat
python3 -m venv venv
source venv/bin/activate
pip install -e ../../
pip install -r requirements.txt

./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata data.json
./manage.py runserver
```

Go to `http://localhost:8000`, select your room, and start chatting! Open as many windows as you'd like.

# Django Hotwire Demo - Reminders

This repository contains a demonstration of [Hotwire](https://hotwired.dev), and
how a site can be built using turbo-frames.

To run this demo, after cloning the repository:

```bash
cd experiments/reminders
python3 -m venv venv
source venv/bin/activate
pip install -e ../../
pip install -r requirements.txt

./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Go to `http://localhost:8000`, and start adding reminders.

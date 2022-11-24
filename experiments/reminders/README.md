# Django Hotwire Demo - Reminders

This repository contains a demonstration of [Hotwire](https://hotwired.dev), and
how a site can be built using turbo-frames.

To run this demo, you'll need to have [a redis server](https://redis.io/docs/getting-started/) running along side. 

For Mac and Linux this is trival, but on windows this will require installing [an ubuntu virtual machine](https://learn.microsoft.com/en-us/windows/wsl/install). See redis docs for details.

Once your redis server is up and running along side, then you can clone the repository and get started:

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

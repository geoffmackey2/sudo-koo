release: python manage.py migrate
web: gunicorn sudokoo.wsgi --preload --log-file -
worker: python manage.py rqworker high default low
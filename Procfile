release: python manage.py collectstatic
release: python manage.py migrate
web: gunicorn commerce.wsgi --log-file -
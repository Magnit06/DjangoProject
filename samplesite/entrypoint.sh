#! /bin/bash

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

python manage.py search_index --rebuild

exec gunicorn samplesite.wsgi:application

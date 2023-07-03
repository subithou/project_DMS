#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

DJANGO_SUPERUSER_PASSWORD=12345 DJANGO_SUPERUSER_USERNAME=pacho DJANGO_SUPERUSER_EMAIL=pacho@gmail.com python manage.py createsuperuser --noinput

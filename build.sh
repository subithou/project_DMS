#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py createsuperuser --username admin --noinput --first_name Admin --noinput


echo "from django.contrib.auth import get_user_model;
User = get_user_model();
user = User.objects.get(username='admin');
user.first_name='Admin';
user.last_name='User';
user.save()" | python manage.py shell 

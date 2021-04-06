#!/bin/sh

python manage.py collectstatic --noinput
python manage.py makemigrations users
python manage.py migrate users
python manage.py makemigrations api_media
python manage.py migrate api_media
python manage.py migrate

exec "$@"
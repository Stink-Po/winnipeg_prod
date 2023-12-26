#!/bin/sh

set -e

# Apply database migrations
python manage.py migrate --noinput --settings=winni_final.settings.prod
python manage.py create_superuser
# Collect static files
python manage.py collectstatic --noinput --settings=winni_final.settings.prod

# Start uWSGI
uwsgi --socket :8000 --master --enable-threads --module winni_final.wsgi

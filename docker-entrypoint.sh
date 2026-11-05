#!/bin/sh
set -eu

cd /app/code
python manage.py migrate --noinput
exec "$@"

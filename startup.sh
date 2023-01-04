#!/usr/bin/env bash

python3 manage.py collectstatic --no-input
python3 manage.py migrate --no-input

gunicorn --bind 0.0.0.0:8000 config.wsgi

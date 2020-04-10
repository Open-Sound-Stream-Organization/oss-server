#!/usr/bin/env bash
cd /oss_server/oss_server
python manage.py migrate
gunicorn --bind :8000 --workers 3 oss_server.wsgi

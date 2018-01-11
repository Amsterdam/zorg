#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

cd /app

source docker-wait.sh

python manage.py migrate --noinput

exec uwsgi


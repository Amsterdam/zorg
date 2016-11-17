#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

cd /app

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini


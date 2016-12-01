#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

cd /app

source docker-wait.sh
source docker-migrate.sh || echo "Could not migrate, ignoring"

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini


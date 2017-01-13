#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

cd /app

source docker-wait.sh
source docker-migrate.sh || echo "Could not migrate, ignoring"
source docker-elastic.sh || echo "Failed to create index"
#source docker-import.sh || echo "Failed to run custom import"

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini


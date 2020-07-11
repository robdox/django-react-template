#!/usr/bin/env bash

echo "Sleeping for 2s to make sure DB is up and running..."
sleep 2s

echo "Migrating the db..."
python manage.py makemigrations
python manage.py migrate

if [ ${DEBUG:=0} -ne 1 ]
then
  echo "Collecting static files into STATIC_ROOT..."
  python manage.py collectstatic --noinput
fi

echo "Running any commands passed to this script from CMD of command..."
exec "$@"

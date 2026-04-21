#!/bin/bash
set -e

COMMANDS="shell utils db sync runserver api match"


if [ -z "$POSTGRES_ADDR" ]; then
  export POSTGRES_ADDR="postgres"
fi

while ! nc -z $POSTGRES_ADDR 5432; do
  echo "Waiting for Postgres server at '$POSTGRES_ADDR' to accept connections on port 5432..."
  sleep 3s
done

if [ "x$MIGRATE" = 'xyes' ]; then
  echo "Running DB CMD: python -m flask db upgrade"
  python -m flask db upgrade
fi

if [ -z "$1" ]; then
  echo "Serving on port 5000"

  exec uwsgi --ini uwsgi.ini --mount "${SCRIPT_NAME}=manage:app"
fi

if [[ $COMMANDS == *"$1"* ]]; then
  exec python -m flask "$@"
fi

exec "$@"

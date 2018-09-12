#!/bin/bash
set -e

COMMANDS="shell utils db sync runserver api match"

STATIC_DIR="/var/local/art17/art17/static/"
TEMP_STATIC_DIR="/var/local/art17/temp_static/"
cp -a $TEMP_STATIC_DIR/. $STATIC_DIR
rm -r $TEMP_STATIC_DIR

if [ -z "$MYSQL_ADDR" ]; then
  MYSQL_ADDR="mysql"
fi

while ! nc -z $MYSQL_ADDR 3306; do
  echo "Waiting for MySQL server at '$MYSQL_ADDR' to accept connections on port 3306..."
  sleep 3s
done

#create database for service
if ! mysql -h $MYSQL_ADDR -u root -p$MYSQL_ROOT_PASSWORD -e "use $DB_NAME;"; then
  echo "CREATE DATABASE $DB_NAME"
  mysql -h $MYSQL_ADDR -u root -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8 COLLATE utf8_general_ci;"
  mysql -h $MYSQL_ADDR -u root -p$MYSQL_ROOT_PASSWORD -e "CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASS';"
  mysql -h $MYSQL_ADDR -u root -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';"
fi

#create binds database for service
if ! mysql -h $MYSQL_ADDR -u root -p$MYSQL_ROOT_PASSWORD -e "use $BIND_NAME;"; then
  echo "CREATE DATABASE $BIND_NAME"
  mysql -h $MYSQL_ADDR -u root -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE $BIND_NAME CHARACTER SET utf8 COLLATE utf8_general_ci;"
  mysql -h $MYSQL_ADDR -u root -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON $BIND_NAME.* TO '$DB_USER'@'%';"
fi

if [ ! -e .skip-db-init ]; then
  touch .skip-db-init
  echo "Running DB CMD: ./manage.py db upgrade"
  python manage.py db upgrade
fi

if [ -z "$1" ]; then
  echo "Serving on port 5000"
  exec gunicorn -e SCRIPT_NAME=$SCRIPT_NAME \
                manage:app \
                --name article17 \
                --bind 0.0.0.0:5000 \
                --access-logfile - \
                --error-logfile -
fi

if [[ $COMMANDS == *"$1"* ]]; then
  exec python manage.py "$@"
fi

exec "$@"

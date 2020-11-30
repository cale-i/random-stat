#!/bin/bash
cd /usr/src/app



# wait for postgres
until psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}\/${POSTGRES_NAME} -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - executing command"

# django settings
if [ ! -e .env ]; then
  python3 /usr/src/app/startup/django_settings/development.py
fi;

# db settings
sed -i -e "s/^DATABASE_URL.*/DATABASE_URL=postgresql:\/\/${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}\/${POSTGRES_NAME}/g" .env
cat .env

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# nginx settings
mv ./startup/nginx.conf /etc/nginx/conf.d/default.conf
service nginx start
gunicorn config.wsgi:application --bind=unix:/var/run/gunicorn/gunicorn.sock
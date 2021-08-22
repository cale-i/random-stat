#!/bin/bash

cd /usr/src/app/startup/db/

# pwd | xargs echo
pip3 install -r requirements.txt

echo "DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_NAME}" > .env
python3 client.py insert_data 

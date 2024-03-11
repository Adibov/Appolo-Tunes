#!/bin/bash

for file in *.up.sql; do
  echo "Applying migration: $file"
  PGPASSWORD=$POSTGRES_PASSWORD \
    psql -h ${POSTGRES_HOST:=db} \
      -U ${POSTGRES_USER:=request_manager} \
      -d ${POSTGRES_DB:=requests_db} < $file
done

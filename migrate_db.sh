#!/bin/bash

for file in migrations/*.up.sql; do
  echo "Applying migration: $file"
  psql -h ${POSTGRES_HOST:=db} -U ${POSTGRES_USER:=request_manager} -d ${POSTGRES_DB:=requests_db} -p $POSTGRES_PASSWORD -f $file
done
```
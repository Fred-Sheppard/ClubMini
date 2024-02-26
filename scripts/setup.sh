#!/bin/bash

echo  'Deleting database'
rm db.sqlite3
echo 'Migrating files'
python manage.py migrate
echo 'Populating database'
sqlite3 db.sqlite3 < scripts/SampleData.sql

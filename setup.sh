#!/bin/bash

rm db.sqlite3
python manage.py migrate
sqlite3 db.sqlite3 < scripts/SampleData.sql
python manage.py runserver

#/bin/bash

echo 'Deleting old migrations'
rm app/migrations/*.py
touch app/migrations/__init__.py
echo 'Creating new migrations'
venv/bin/python manage.py makemigrations

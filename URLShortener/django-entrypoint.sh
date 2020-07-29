#!/bin/bash
#echo "Collect Static Files"
#python manage.py collectstatic
echo "Start Migrations..."
python manage.py migrate
exec "$@"



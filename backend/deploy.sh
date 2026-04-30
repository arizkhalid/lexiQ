#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading database fixture..."
python manage.py loaddata seed_data.json

echo "Deployment complete!"

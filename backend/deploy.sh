#!/bin/bash
set -e

cd backend

echo "Running migrations..."
python manage.py migrate --noinput
echo "✓ Migrations done"

echo "Checking for seed_data.json..."
if [ -f "seed_data.json" ]; then
    echo "✓ Found seed_data.json"
    echo "Loading database fixture..."
    python manage.py loaddata seed_data.json --verbosity 2
    echo "✓ Data loaded"
else
    echo "✗ seed_data.json not found!"
    exit 1
fi

echo "✓ Deployment complete!"

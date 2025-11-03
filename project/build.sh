#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations (SQLite)
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create admin user if it doesn't exist
echo "Creating admin user..."
python manage.py createadmin

echo "Build completed successfully!"

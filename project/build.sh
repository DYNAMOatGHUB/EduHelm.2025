#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Delete old database if exists (fresh start for schema changes)
echo "Cleaning up old database..."
rm -f db.sqlite3

# Run database migrations (SQLite)
echo "Running migrations..."
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create admin user if it doesn't exist
echo "Creating admin user..."
python manage.py createadmin

# Reset admin password to ensure it matches the default
echo "Resetting admin password..."
python manage.py resetadmin

echo "Build completed successfully!"

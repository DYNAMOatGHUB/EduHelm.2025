#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Handle courses app migration reset (fresh database structure)
echo "Resetting courses app migrations..."
python manage.py migrate courses zero --noinput || echo "No previous courses migrations to revert"

# Run database migrations (SQLite)
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

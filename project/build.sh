#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Database migration strategy for Render deployment
echo "Handling migrations..."

# Check if we have migration inconsistency and fix it
# This script handles the case where users.0003 was applied before courses.0001
if python manage.py showmigrations users | grep -q "\[X\] 0003_auto_20251031_1412"; then
    echo "Detected migration inconsistency. Fixing..."
    
    # Unapply users migrations that depend on courses
    python manage.py migrate users 0002_rename_profiole_profile --fake || true
    
    # Now apply courses migrations first
    python manage.py migrate courses || true
    
    # Then apply all migrations
    python manage.py migrate
else
    # Normal migration flow
    python manage.py migrate
fi

# Collect static files
python manage.py collectstatic --no-input

# Create admin user if it doesn't exist
echo "Creating admin user..."
python manage.py createadmin

# Reset admin password to ensure it matches the default
echo "Resetting admin password..."
python manage.py resetadmin

echo "Build completed successfully!"

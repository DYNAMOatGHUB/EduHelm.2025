#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Database migration strategy for Render deployment
echo "Handling migrations..."

# Create a Python script to fix migration inconsistency directly in the database
python << 'END_PYTHON'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        # Check if users.0003 is in the migration table
        cursor.execute(
            "SELECT id FROM django_migrations WHERE app='users' AND name='0003_auto_20251031_1412'"
        )
        users_003_exists = cursor.fetchone()
        
        # Check if courses.0001 is in the migration table
        cursor.execute(
            "SELECT id FROM django_migrations WHERE app='courses' AND name='0001_initial'"
        )
        courses_001_exists = cursor.fetchone()
        
        if users_003_exists and not courses_001_exists:
            print("Detected migration inconsistency. Fixing by removing users.0003 from history...")
            # Remove the problematic migration from history
            cursor.execute(
                "DELETE FROM django_migrations WHERE app='users' AND name='0003_auto_20251031_1412'"
            )
            cursor.execute(
                "DELETE FROM django_migrations WHERE app='users' AND name='0004_studyschedule'"
            )
            cursor.execute(
                "DELETE FROM django_migrations WHERE app='users' AND name='0005_alter_badge_id_alter_discussion_id_and_more'"
            )
            print("Removed problematic migration records. Will reapply them with correct dependency order.")
        else:
            print("No migration inconsistency detected or already fixed.")
            
except Exception as e:
    print(f"Could not check/fix migrations (this is OK if first deployment): {e}")
END_PYTHON

# Now run migrations normally
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

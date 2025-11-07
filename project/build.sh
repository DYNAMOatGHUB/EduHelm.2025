#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Database migration strategy for Render deployment
echo "Handling migrations..."

# Create a Python script to comprehensively fix all migration issues
python << 'END_PYTHON'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        # Get all existing tables to understand database state
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' AND tablename LIKE 'users_%'
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"Found {len(existing_tables)} existing users tables")
        
        # Check migration state
        cursor.execute(
            "SELECT app, name FROM django_migrations ORDER BY app, name"
        )
        existing_migrations = cursor.fetchall()
        print(f"Existing migrations: {existing_migrations}")
        
        # If users tables exist but courses.0001 is not in migrations, we have the inconsistency
        has_users_tables = any('users_' in t for t in existing_tables)
        
        cursor.execute(
            "SELECT COUNT(*) FROM django_migrations WHERE app='courses' AND name='0001_initial'"
        )
        has_courses_migration = cursor.fetchone()[0] > 0
        
        if has_users_tables and not has_courses_migration:
            print("DATABASE INCONSISTENCY DETECTED!")
            print("Tables exist but migration history is incomplete. Fixing...")
            
            # Strategy: Mark all migrations as applied since tables exist
            # This is safe because --fake-initial will handle it
            
            # First, ensure courses.0001_initial is marked as applied
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES ('courses', '0001_initial', NOW())
                ON CONFLICT DO NOTHING
            """)
            
            # Then ensure users migrations are marked as applied
            users_migrations = [
                '0003_auto_20251031_1412',
                '0004_studyschedule',
                '0005_alter_badge_id_alter_discussion_id_and_more'
            ]
            
            for migration in users_migrations:
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied)
                    VALUES ('users', %s, NOW())
                    ON CONFLICT DO NOTHING
                """, [migration])
            
            print("✅ Migration history fixed! All existing migrations marked as applied.")
        else:
            print("✅ Database is in consistent state.")
            
except Exception as e:
    print(f"Migration check/fix encountered an issue: {e}")
    print("Will proceed with standard migration...")
END_PYTHON

# Now run migrations with --fake-initial as safety net
python manage.py migrate --fake-initial

# Collect static files
python manage.py collectstatic --no-input

# Create admin user if it doesn't exist
echo "Creating admin user..."
python manage.py createadmin

# Reset admin password to ensure it matches the default
echo "Resetting admin password..."
python manage.py resetadmin

echo "Build completed successfully!"

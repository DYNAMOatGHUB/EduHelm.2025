"""
Fix MongoDB Profile Collection Issue
This script drops and recreates the users_profile collection to fix the duplicate key error.
"""

import pymongo
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.conf import settings

# MongoDB connection
client = pymongo.MongoClient(settings.DATABASES['default']['CLIENT']['host'])
db = client[settings.DATABASES['default']['NAME']]

print("=" * 60)
print("FIXING USERS_PROFILE COLLECTION")
print("=" * 60)

# Drop the problematic collection
if 'users_profile' in db.list_collection_names():
    print("\n1. Dropping existing users_profile collection...")
    db['users_profile'].drop()
    print("   ✅ Collection dropped")
else:
    print("\n1. users_profile collection doesn't exist yet")

# Create fresh collection
print("\n2. Creating fresh users_profile collection...")
db.create_collection('users_profile')
print("   ✅ Collection created")

# Verify
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)
print(f"\nTotal collections: {len(db.list_collection_names())}")

if 'users_profile' in db.list_collection_names():
    count = db['users_profile'].count_documents({})
    print(f"✅ users_profile exists (documents: {count})")
else:
    print("❌ users_profile NOT found")

print("\n" + "=" * 60)
print("✅ FIX COMPLETE")
print("=" * 60)
print("\nNext steps:")
print("  1. Register a new user to test")
print("  2. Profile should auto-create without errors")
print("=" * 60)

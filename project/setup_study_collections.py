"""
Script to create StudySession and StudyGoal collections in MongoDB
"""
import pymongo
import sys
import os
from datetime import datetime

# MongoDB connection
client = pymongo.MongoClient('localhost', 27017)
db = client['eduhelm_db']

print("Creating StudySession and StudyGoal collections...")

# Check if collections exist
collections = db.list_collection_names()
print(f"Existing collections: {collections}")

# Create StudySession collection if it doesn't exist
if 'users_studysession' not in collections:
    db.create_collection('users_studysession')
    print("✓ Created users_studysession collection")
else:
    print("✓ users_studysession collection already exists")

# Create StudyGoal collection if it doesn't exist
if 'users_studygoal' not in collections:
    db.create_collection('users_studygoal')
    print("✓ Created users_studygoal collection")
else:
    print("✓ users_studygoal collection already exists")

# Update Profile collection schema (add new fields if needed)
print("\nUpdating Profile collection...")
profiles = db.users_profile.find()
count = 0
for profile in profiles:
    update_fields = {}
    
    if 'last_study_date' not in profile:
        update_fields['last_study_date'] = None
    
    if update_fields:
        db.users_profile.update_one(
            {'_id': profile['_id']},
            {'$set': update_fields}
        )
        count += 1

if count > 0:
    print(f"✓ Updated {count} profile(s) with new fields")
else:
    print("✓ All profiles up to date")

print("\n✅ Database setup complete!")
print(f"Total collections: {len(db.list_collection_names())}")

client.close()

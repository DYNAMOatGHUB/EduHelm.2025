import os
import sys
import django
from pymongo import MongoClient

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client['eduhelm_db']

print("=" * 60)
print("PHASE 4: Notes & Resources Collections Setup")
print("=" * 60)

# Create NoteCategory collection
print("\n1. Creating users_notecategory collection...")
try:
    if 'users_notecategory' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_notecategory')
        print("   ✅ users_notecategory collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Create StudyNote collection
print("\n2. Creating users_studynote collection...")
try:
    if 'users_studynote' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_studynote')
        print("   ✅ users_studynote collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Create SharedResource collection
print("\n3. Creating users_sharedresource collection...")
try:
    if 'users_sharedresource' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_sharedresource')
        print("   ✅ users_sharedresource collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Verify collections
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)
collections = db.list_collection_names()
phase4_collections = [
    'users_notecategory',
    'users_studynote',
    'users_sharedresource'
]

print(f"\nTotal collections in database: {len(collections)}")
print("\nPhase 4 Collections Status:")
for coll in phase4_collections:
    status = "✅ EXISTS" if coll in collections else "❌ MISSING"
    print(f"  {status} - {coll}")

# Sample data structure for reference
print("\n" + "=" * 60)
print("COLLECTION SCHEMAS (Reference)")
print("=" * 60)

print("\n📁 NoteCategory Schema:")
print("""
{
    user_id: ObjectId,
    name: String (max 100),
    color: String (hex, default '#4CAF50'),
    icon: String (FontAwesome class, default 'fas fa-folder'),
    description: Text,
    created_at: DateTime
}
""")

print("\n📝 StudyNote Schema:")
print("""
{
    user_id: ObjectId,
    course_id: ObjectId (nullable),
    category_id: ObjectId (nullable),
    title: String (max 200),
    content: Text (markdown supported),
    tags: String (comma-separated),
    is_pinned: Boolean,
    is_favorite: Boolean,
    created_at: DateTime,
    updated_at: DateTime
}
""")

print("\n📚 SharedResource Schema:")
print("""
{
    user_id: ObjectId,
    course_id: ObjectId (nullable),
    title: String (max 200),
    description: Text,
    resource_type: String (pdf/video/link/image/audio/other),
    file: String (file path),
    url: String (URL, max 500),
    file_size: BigInteger (bytes),
    downloads: Integer,
    views: Integer,
    is_public: Boolean,
    created_at: DateTime,
    updated_at: DateTime
}
""")

print("\n" + "=" * 60)
print("✅ PHASE 4 MONGODB SETUP COMPLETE")
print("=" * 60)
print("\nNext Steps:")
print("  1. Test note creation in Django")
print("  2. Test category management")
print("  3. Test resource uploads")
print("  4. Verify all CRUD operations")
print("\n")

client.close()

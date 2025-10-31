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
print("PHASE 5: Collaborative Learning Collections Setup")
print("=" * 60)

# Create StudyGroup collection
print("\n1. Creating users_studygroup collection...")
try:
    if 'users_studygroup' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_studygroup')
        print("   ✅ users_studygroup collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Create GroupMembership collection
print("\n2. Creating users_groupmembership collection...")
try:
    if 'users_groupmembership' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_groupmembership')
        print("   ✅ users_groupmembership collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Create Discussion collection
print("\n3. Creating users_discussion collection...")
try:
    if 'users_discussion' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_discussion')
        print("   ✅ users_discussion collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Create DiscussionReply collection
print("\n4. Creating users_discussionreply collection...")
try:
    if 'users_discussionreply' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_discussionreply')
        print("   ✅ users_discussionreply collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Create PeerReview collection
print("\n5. Creating users_peerreview collection...")
try:
    if 'users_peerreview' in db.list_collection_names():
        print("   ⚠️  Collection already exists")
    else:
        db.create_collection('users_peerreview')
        print("   ✅ users_peerreview collection created")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Verify collections
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)
collections = db.list_collection_names()
phase5_collections = [
    'users_studygroup',
    'users_groupmembership',
    'users_discussion',
    'users_discussionreply',
    'users_peerreview'
]

print(f"\nTotal collections in database: {len(collections)}")
print("\nPhase 5 Collections Status:")
for coll in phase5_collections:
    status = "✅ EXISTS" if coll in collections else "❌ MISSING"
    print(f"  {status} - {coll}")

# Sample data structure for reference
print("\n" + "=" * 60)
print("COLLECTION SCHEMAS (Reference)")
print("=" * 60)

print("\n👥 StudyGroup Schema:")
print("""
{
    name: String (max 200),
    description: Text,
    creator_id: ObjectId,
    max_members: Integer (default 10),
    is_private: Boolean,
    cover_image: String (file path),
    course_id: ObjectId (nullable),
    created_at: DateTime,
    updated_at: DateTime
}
""")

print("\n🎫 GroupMembership Schema:")
print("""
{
    user_id: ObjectId,
    group_id: ObjectId,
    role: String (admin/moderator/member),
    joined_at: DateTime
}
""")

print("\n💬 Discussion Schema:")
print("""
{
    group_id: ObjectId,
    author_id: ObjectId,
    title: String (max 200),
    content: Text,
    is_pinned: Boolean,
    is_locked: Boolean,
    created_at: DateTime,
    updated_at: DateTime
}
""")

print("\n💭 DiscussionReply Schema:")
print("""
{
    discussion_id: ObjectId,
    author_id: ObjectId,
    content: Text,
    parent_id: ObjectId (nullable, for threading),
    created_at: DateTime,
    updated_at: DateTime
}
""")

print("\n⭐ PeerReview Schema:")
print("""
{
    reviewer_id: ObjectId,
    note_id: ObjectId (nullable),
    resource_id: ObjectId (nullable),
    rating: Integer (1-5),
    feedback: Text,
    helpful_count: Integer,
    created_at: DateTime,
    updated_at: DateTime
}
""")

print("\n" + "=" * 60)
print("✅ PHASE 5 MONGODB SETUP COMPLETE")
print("=" * 60)
print("\nNext Steps:")
print("  1. Create Phase 5 templates")
print("  2. Test group creation")
print("  3. Test discussions")
print("  4. Test peer reviews")
print("\n")

client.close()

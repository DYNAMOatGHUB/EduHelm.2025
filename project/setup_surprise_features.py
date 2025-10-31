"""
Setup script for new surprise features:
- Create MongoDB collections
- Seed achievement badges
- Create sample notifications
"""
import os
import django
import pymongo

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.conf import settings
from users.models import Badge, Notification, UserActivity
from django.contrib.auth.models import User

# MongoDB connection
client = pymongo.MongoClient(settings.DATABASES['default']['CLIENT']['host'])
db = client[settings.DATABASES['default']['NAME']]

print("=" * 70)
print("🎉 SETTING UP SURPRISE FEATURES")
print("=" * 70)

# Create MongoDB collections
print("\n📦 Creating MongoDB Collections...")
collections_to_create = [
    'users_badge',
    'users_userbadge',
    'users_notification',
    'users_useractivity',
]

for collection_name in collections_to_create:
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        print(f"   ✅ Created: {collection_name}")
    else:
        print(f"   ✓ Exists: {collection_name}")

# Seed Achievement Badges
print("\n🏆 Creating Achievement Badges...")

badges_data = [
    # Study Milestones
    {
        'name': '🔥 First Steps',
        'description': 'Complete your first study session',
        'icon': 'fa-fire',
        'badge_type': 'study',
        'color': '#FF6B6B',
        'requirement': 1
    },
    {
        'name': '⏰ 10 Hour Hero',
        'description': 'Study for 10 total hours',
        'icon': 'fa-clock',
        'badge_type': 'study',
        'color': '#4ECDC4',
        'requirement': 10
    },
    {
        'name': '📚 Century Scholar',
        'description': 'Study for 100 total hours',
        'icon': 'fa-book',
        'badge_type': 'study',
        'color': '#FFD93D',
        'requirement': 100
    },
    {
        'name': '🎯 7 Day Streak',
        'description': 'Maintain a 7-day study streak',
        'icon': 'fa-bullseye',
        'badge_type': 'study',
        'color': '#6BCB77',
        'requirement': 7
    },
    {
        'name': '🚀 30 Day Champion',
        'description': 'Achieve a 30-day study streak!',
        'icon': 'fa-rocket',
        'badge_type': 'study',
        'color': '#9D5BD2',
        'requirement': 30
    },
    
    # Social Engagement
    {
        'name': '👥 Team Player',
        'description': 'Join your first study group',
        'icon': 'fa-users',
        'badge_type': 'social',
        'color': '#FF9F1C',
        'requirement': 1
    },
    {
        'name': '💬 Discussion Starter',
        'description': 'Post 10 discussions',
        'icon': 'fa-comments',
        'badge_type': 'social',
        'color': '#2EC4B6',
        'requirement': 10
    },
    {
        'name': '⭐ Helpful Peer',
        'description': 'Give 25 peer reviews',
        'icon': 'fa-star',
        'badge_type': 'social',
        'color': '#FFB627',
        'requirement': 25
    },
    
    # Skill Mastery
    {
        'name': '📝 Note Taker',
        'description': 'Create 10 study notes',
        'icon': 'fa-edit',
        'badge_type': 'skill',
        'color': '#4A90E2',
        'requirement': 10
    },
    {
        'name': '📂 Resource Master',
        'description': 'Share 20 resources',
        'icon': 'fa-folder',
        'badge_type': 'skill',
        'color': '#F39C12',
        'requirement': 20
    },
    {
        'name': '🎓 Course Enthusiast',
        'description': 'Enroll in 5 courses',
        'icon': 'fa-graduation-cap',
        'badge_type': 'skill',
        'color': '#E74C3C',
        'requirement': 5
    },
    
    # Special Achievements
    {
        'name': '🌟 Early Adopter',
        'description': 'One of the first users!',
        'icon': 'fa-certificate',
        'badge_type': 'special',
        'color': '#9B59B6',
        'requirement': 1
    },
    {
        'name': '👑 Master Student',
        'description': 'Earn 10 different badges',
        'icon': 'fa-crown',
        'badge_type': 'special',
        'color': '#F1C40F',
        'requirement': 10
    },
]

created_count = 0
for badge_data in badges_data:
    badge, created = Badge.objects.get_or_create(
        name=badge_data['name'],
        defaults=badge_data
    )
    if created:
        created_count += 1
        print(f"   ✅ Created: {badge.name}")
    else:
        print(f"   ✓ Exists: {badge.name}")

print(f"\n   📊 Total badges: {Badge.objects.count()} ({created_count} new)")

# Create welcome notifications for all users
print("\n🔔 Creating Welcome Notifications...")

welcome_message = """
🎉 Welcome to EduHelm - Your AI Study Companion!

Explore these amazing features:
• 📚 Track your study sessions with our smart timer
• 📝 Create organized notes with categories
• 👥 Join study groups and collaborate
• 🏆 Earn badges and track your progress
• 📊 View detailed analytics of your learning journey

Start studying today to earn your first badge!
"""

users = User.objects.all()
notif_count = 0
for user in users:
    # Check if welcome notification already exists
    if not Notification.objects.filter(user=user, notification_type='system', title='Welcome to EduHelm! 🎉').exists():
        Notification.objects.create(
            user=user,
            notification_type='system',
            title='Welcome to EduHelm! 🎉',
            message=welcome_message,
            link='/study/dashboard/'
        )
        notif_count += 1
        print(f"   ✅ Created welcome notification for {user.username}")
    else:
        print(f"   ✓ Already exists for {user.username}")

# Verify MongoDB collections
print("\n📊 Verifying MongoDB Collections...")
total_collections = len(db.list_collection_names())
print(f"   Total collections: {total_collections}")

# Check new collections
new_collections = ['users_badge', 'users_userbadge', 'users_notification', 'users_useractivity']
for col in new_collections:
    if col in db.list_collection_names():
        count = db[col].count_documents({})
        print(f"   ✅ {col}: {count} documents")
    else:
        print(f"   ❌ {col}: NOT FOUND!")

print("\n" + "=" * 70)
print("✅ SURPRISE FEATURES SETUP COMPLETE!")
print("=" * 70)
print("\n🎯 Next Steps:")
print("   1. Restart your Django server")
print("   2. Login to see your new notifications")
print("   3. Check out the shiny new dashboard!")
print("   4. Start studying to earn badges!")
print("\n" + "=" * 70)

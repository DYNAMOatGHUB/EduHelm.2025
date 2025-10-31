"""Force clean all duplicate profiles - keep only one per user"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from users.models import Profile
from django.contrib.auth.models import User

print("=" * 60)
print("CLEANING DUPLICATE PROFILES")
print("=" * 60)

all_users = User.objects.all()
print(f"\nTotal users: {all_users.count()}")
print(f"Total profiles BEFORE cleanup: {Profile.objects.count()}")

for user in all_users:
    profiles = Profile.objects.filter(user=user)
    count = profiles.count()
    
    if count == 0:
        # No profile - create one
        Profile.objects.create(user=user)
        print(f"  {user.username}: Created new profile")
    elif count == 1:
        # Perfect - one profile
        print(f"  {user.username}: ✅ OK (1 profile)")
    else:
        # Duplicates - keep first, delete rest
        first_profile = profiles.first()
        duplicates = profiles.exclude(id=first_profile.id)
        duplicate_count = duplicates.count()
        duplicates.delete()
        print(f"  {user.username}: ❌ Fixed (deleted {duplicate_count} duplicates)")

print(f"\nTotal profiles AFTER cleanup: {Profile.objects.count()}")
print("=" * 60)
print("✅ CLEANUP COMPLETE!")
print("=" * 60)

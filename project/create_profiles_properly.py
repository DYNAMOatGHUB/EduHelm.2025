"""Create profiles the RIGHT way with proper MongoDB IDs"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from users.models import Profile
from django.contrib.auth.models import User

print("=" * 60)
print("CREATING PROFILES WITH PROPER IDS")
print("=" * 60)

# First, delete ALL profiles
Profile.objects.all().delete()
print(f"Deleted all existing profiles\n")

# Disable signals temporarily to avoid loops
from django.db.models.signals import post_save
from users import signals

# Disconnect the signals
post_save.disconnect(signals.create_profile, sender=User)
# post_save.disconnect(signals.save_profile, sender=User)  # Already commented out

for user in User.objects.all():
    # Create profile normally - signals are disabled
    profile = Profile.objects.create(user=user)
    print(f"✅ Created profile for {user.username}")

# Reconnect signals
post_save.connect(signals.create_profile, sender=User)

print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)

print(f"\nTotal users: {User.objects.count()}")
print(f"Total profiles: {Profile.objects.count()}")

print("\nUser-Profile Mapping:")
for user in User.objects.all():
    try:
        profile = Profile.objects.get(user=user)
        print(f"  ✅ {user.username} -> Profile ID: {profile.id}")
    except Profile.DoesNotExist:
        print(f"  ❌ {user.username} -> NO PROFILE!")
    except Profile.MultipleObjectsReturned:
        print(f"  ⚠️ {user.username} -> MULTIPLE PROFILES!")

print("\n" + "=" * 60)
print("✅ COMPLETE!")
print("=" * 60)

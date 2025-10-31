from django.contrib.auth.models import User
from django.db.models.signals import post_save   #fires a signal when the user is created
from django.dispatch import receiver
from .models import Profile

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Commenting out save_profile to prevent duplicate creation loops
# @receiver(post_save,sender=User)
# def save_profile(sender, instance, created=False, **kwargs):
#     # Only save if not just created (create_profile handles new users)
#     if not created:
#         try:
#             # Check how many profiles exist
#             profiles = Profile.objects.filter(user=instance)
#             count = profiles.count()
#             
#             if count == 0:
#                 # No profile - create one
#                 Profile.objects.create(user=instance)
#             elif count == 1:
#                 # Perfect - save it
#                 profiles.first().save()
#             else:
#                 # Duplicates - keep first, delete rest
#                 all_profiles = list(profiles)  # Convert to list to get stable ordering
#                 keep_profile = all_profiles[0]
#                 for duplicate in all_profiles[1:]:
#                     duplicate.delete()
#                 keep_profile.save()
#         except Exception as e:
#             # Log error but don't crash
#             import logging
#             logging.error(f"Error in save_profile signal: {e}")
"""Create clean profiles for all users"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from users.models import Profile
from django.contrib.auth.models import User

print('Creating clean profiles...')
for user in User.objects.all():
    profile, created = Profile.objects.get_or_create(user=user)
    status = "Created" if created else "Already exists"
    print(f'  {user.username}: {status}')

print(f'\nFinal count: {User.objects.count()} users, {Profile.objects.count()} profiles')
print('✅ All users have profiles!')

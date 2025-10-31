from users.models import User, Profile

# Get admin user
user = User.objects.get(username='admin')

# Create profile
profile, created = Profile.objects.get_or_create(user=user)

if created:
    print('✅ Profile created for admin user!')
else:
    print('✅ Profile already exists for admin user')

print(f'\nUser: {user.username}')
print(f'Email: {user.email}')
print(f'Profile: {profile}')

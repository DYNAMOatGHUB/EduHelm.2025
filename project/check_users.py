import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['eduhelm_db']

print('\n' + '='*70)
print('👥 EXISTING USERS IN DATABASE')
print('='*70 + '\n')

users = list(db.auth_user.find({}, {'username': 1, 'email': 1, 'is_superuser': 1, 'is_staff': 1}))

if not users:
    print('❌ No users found in database!\n')
    print('You need to create a superuser first.')
    print('\nRun this command:')
    print('python manage.py createsuperuser')
else:
    for i, user in enumerate(users, 1):
        print(f'{i}. USERNAME: {user["username"]}')
        print(f'   Email: {user.get("email", "N/A")}')
        print(f'   Superuser: {"✅ Yes" if user.get("is_superuser") else "❌ No"}')
        print(f'   Staff: {"✅ Yes" if user.get("is_staff") else "❌ No"}')
        print()

print('='*70)
print(f'Total Users: {len(users)}')
print('='*70)

print('\n💡 LOGIN INFORMATION:')
print('─'*70)
if users:
    print('\nYou can login with any of the usernames above.')
    print('\n⚠️  PASSWORDS are encrypted in the database.')
    print('    If you forgot your password, use one of these options:\n')
    print('    Option 1 - Reset via Django shell:')
    print('    python manage.py shell')
    print('    >>> from django.contrib.auth.models import User')
    print('    >>> user = User.objects.get(username="admin")')
    print('    >>> user.set_password("newpassword123")')
    print('    >>> user.save()\n')
    print('    Option 2 - Create new superuser:')
    print('    python manage.py createsuperuser')
else:
    print('\n🚀 CREATE YOUR FIRST USER:')
    print('   python manage.py createsuperuser')

print('\n📍 LOGIN URL: http://127.0.0.1:8000/login/')
print('='*70 + '\n')

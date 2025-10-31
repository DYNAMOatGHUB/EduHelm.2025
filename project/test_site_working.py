"""
Test all views to ensure they work without errors
Run this to diagnose which pages are causing issues
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from users.models import Profile

print("=" * 60)
print("TESTING SITE FUNCTIONALITY")
print("=" * 60)

# Create test client
client = Client()

# Test public pages
print("\n1. Testing Public Pages...")
public_urls = [
    ('/', 'Homepage'),
    ('/login/', 'Login Page'),
    ('/register/', 'Register Page'),
]

for url, name in public_urls:
    try:
        response = client.get(url)
        status = "✅ OK" if response.status_code in [200, 302] else f"❌ ERROR ({response.status_code})"
        print(f"   {name}: {status}")
    except Exception as e:
        print(f"   {name}: ❌ EXCEPTION - {str(e)[:50]}")

# Ensure test user exists with profile
print("\n2. Checking Test User...")
try:
    user = User.objects.get(username='testuser')
    profile, created = Profile.objects.get_or_create(user=user)
    print(f"   ✅ User 'testuser' exists")
    print(f"   ✅ Profile {'created' if created else 'already exists'}")
except User.DoesNotExist:
    print("   ⚠️ Creating test user...")
    user = User.objects.create_user('testuser', 'test@test.com', 'test123')
    profile = Profile.objects.create(user=user)
    print("   ✅ Test user created")

# Login and test protected pages
print("\n3. Testing Protected Pages (logged in)...")
login_success = client.login(username='testuser', password='test123')
if login_success:
    print("   ✅ Login successful")
    
    protected_urls = [
        ('/profile/', 'Profile Page'),
        ('/study/dashboard/', 'Study Dashboard'),
        ('/study/history/', 'Study History'),
        ('/study/analytics/', 'Study Analytics'),
        ('/notes/', 'Notes List'),
        ('/resources/', 'Resources Library'),
        ('/groups/', 'Study Groups'),
        ('/courses/', 'Courses'),
    ]
    
    for url, name in protected_urls:
        try:
            response = client.get(url)
            status = "✅ OK" if response.status_code in [200, 302] else f"❌ ERROR ({response.status_code})"
            print(f"   {name}: {status}")
            
            # If error, show more details
            if response.status_code not in [200, 302]:
                if hasattr(response, 'content'):
                    error_msg = str(response.content[:200])
                    print(f"      Error: {error_msg}")
        except Exception as e:
            print(f"   {name}: ❌ EXCEPTION")
            print(f"      {str(e)[:100]}")
else:
    print("   ❌ Login failed!")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nIf all tests show ✅, your site is working!")
print("If you see ❌, that page needs fixing.")

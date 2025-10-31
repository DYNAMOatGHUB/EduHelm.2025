"""
Diagnose what error is happening when accessing pages
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from users import views

print("=" * 70)
print("DIAGNOSING SITE ERRORS")
print("=" * 70)

# Test 1: Can we access homepage?
print("\n1. Testing Homepage (/)...")
client = Client()
try:
    response = client.get('/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Homepage works!")
    elif response.status_code == 302:
        print(f"   → Redirects to: {response.url}")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Exception: {str(e)[:100]}")

# Test 2: Can logged-out user access profile?
print("\n2. Testing Profile Page (not logged in)...")
try:
    response = client.get('/profile/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:
        print(f"   → Redirects to login (expected): {response.url}")
        print("   ✅ Login redirect works!")
    else:
        print(f"   ❌ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Exception: {type(e).__name__}: {str(e)[:150]}")
    import traceback
    traceback.print_exc()

# Test 3: Can logged-in user access profile?
print("\n3. Testing Profile Page (logged in as testuser)...")
try:
    # Try to login
    login_success = client.login(username='testuser', password='test123')
    if login_success:
        print("   ✅ Login successful")
        
        # Try to access profile
        response = client.get('/profile/')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Profile page loads!")
        else:
            print(f"   ❌ Error status: {response.status_code}")
            if hasattr(response, 'content'):
                error_preview = response.content[:500].decode('utf-8', errors='ignore')
                print(f"   Error content preview: {error_preview[:200]}")
    else:
        print("   ❌ Login failed - check testuser password")
except Exception as e:
    print(f"   ❌ EXCEPTION CAUGHT:")
    print(f"   Type: {type(e).__name__}")
    print(f"   Message: {str(e)[:200]}")
    print("\n   Full Traceback:")
    import traceback
    traceback.print_exc()

# Test 4: Check all users have profiles
print("\n4. Checking User-Profile Relationships...")
from users.models import Profile
for user in User.objects.all():
    try:
        profile_count = Profile.objects.filter(user=user).count()
        if profile_count == 1:
            print(f"   ✅ {user.username}: 1 profile")
        elif profile_count == 0:
            print(f"   ❌ {user.username}: NO PROFILE!")
        else:
            print(f"   ⚠️  {user.username}: {profile_count} profiles (DUPLICATES!)")
    except Exception as e:
        print(f"   ❌ {user.username}: Error checking profile - {str(e)[:50]}")

print("\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)
print("\nIf you see exceptions above, that's your problem!")
print("The traceback will show exactly which line is failing.")

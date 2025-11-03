from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Profile
import os

# Create your views here.

def home(request):
    # Auto-create admin user on first visit if it doesn't exist
    try:
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        if not User.objects.filter(username=admin_username).exists():
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@eduhelm.com')
            admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin@2025')
            
            admin = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            
            Profile.objects.get_or_create(
                user=admin,
                defaults={
                    'bio': 'System Administrator',
                    'is_mentor': True
                }
            )
    except Exception as e:
        # Silently fail - admin creation will be retried on next request
        pass
    
    return render(request, 'sample/home.html')


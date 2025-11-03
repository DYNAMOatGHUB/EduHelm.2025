# Render Post-Deployment Steps

## ✅ All Issues Fixed!

### What was fixed:
1. **Removed dj-database-url** - Caused Django version conflict with djongo
2. **Removed unused import** - Fixed ModuleNotFoundError in settings.py
3. **Updated static files storage** - Changed to `CompressedStaticFilesStorage` (safer than Manifest version)
4. **Added security settings** - CSRF, SSL redirect, secure cookies (production only)
5. **Updated .gitignore** - Added .env and staticfiles/

### After Successful Deploy:

#### 1. Create Admin User (via Render Shell)
```bash
# In Render Dashboard > Shell
python manage.py shell

# Then in the Python shell:
from django.contrib.auth.models import User
from users.models import Profile

# Create admin user
admin = User.objects.create_superuser(
    username='admin',
    email='admin@eduhelm.com',
    password='CHANGE_THIS_PASSWORD'
)

# Create profile for admin
profile = Profile.objects.create(
    user=admin,
    bio='System Administrator',
    is_mentor=True
)

print(f"✅ Admin user created: {admin.username}")
exit()
```

#### 2. Verify Site Works
- Visit your Render URL (e.g., https://your-app.onrender.com)
- Check home page loads
- Check static files (CSS, logo) are served correctly
- Test login with admin credentials
- Test registration flow
- Create a test course if needed

#### 3. Monitor Logs
```bash
# In Render Dashboard
- Check "Logs" tab for any errors
- Look for successful requests
- Verify no 500 errors
```

#### 4. Environment Variables (Already Set)
✅ SECRET_KEY
✅ DEBUG=False
✅ ALLOWED_HOSTS
✅ MONGODB_URI
✅ MONGODB_NAME
✅ PYTHON_VERSION

#### 5. Optional: Custom Domain
- Follow CUSTOM_DOMAIN_SETUP.md for local development
- For production, add custom domain in Render dashboard

## Current Deployment Status
- ✅ Requirements conflict resolved
- ✅ Import error fixed
- ✅ Static files configuration optimized
- ✅ Security settings added
- ✅ Code pushed to GitHub (commit: 88a2fcd)
- ⏳ Waiting for Render auto-deploy

## Troubleshooting

### If collectstatic fails:
```bash
# Check that all templates reference static files correctly
# Ensure {% load static %} is at the top of templates
```

### If MongoDB connection fails:
- Verify MONGODB_URI in Render env vars
- Check MongoDB Atlas network access (allow 0.0.0.0/0)
- Verify database user credentials

### If 502/503 errors:
- Check Render logs for Python errors
- Verify gunicorn is starting correctly
- Check ALLOWED_HOSTS includes your Render domain

## Next Steps After Live
1. Create admin user (see above)
2. Test all major flows
3. Upload test content (courses, lessons)
4. Consider setting up:
   - Email backend (for password reset)
   - Media file storage (AWS S3 or similar)
   - Regular database backups
   - Monitoring/alerting

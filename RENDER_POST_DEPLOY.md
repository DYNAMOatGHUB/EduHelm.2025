# EduHelm - Deployment Guide

## ✅ Your Site is Live!

**Live URL:** https://eduhelm-2025.onrender.com

## Current Setup

- **Platform:** Render (Free Tier)
- **Framework:** Django 3.1.12
- **Database:** SQLite (file-based)
- **Static Files:** WhiteNoise
- **Python:** 3.11.9

## Login Credentials

- **URL:** https://eduhelm-2025.onrender.com/login
- **Username:** `admin`
- **Password:** `Admin@2025` (or custom password set in ADMIN_PASSWORD env var)

## Important Notes

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after sleep takes ~50 seconds to wake up
- **Media files (uploads) are ephemeral** - lost on redeploy/restart
- Database persists between deploys but not if service is deleted

### Media Files (Profile Photos, etc.)
**Problem:** Uploaded files don't persist on Render's free tier.

**Solutions:**
1. **Accept the limitation** - Re-upload files after each deploy
2. **Use Cloudinary** - Free tier: 25GB storage, easy integration
3. **Upgrade to Render's paid plan** - Get persistent disk storage

### Post-Deployment Checklist

1. ✅ Site is accessible at https://eduhelm-2025.onrender.com
2. ✅ Admin user created automatically during build
3. ✅ Static files (CSS, JS, logo) loading correctly
4. ✅ Login/logout functionality works
5. ⚠️ Upload a profile photo (will be lost on next deploy)

## Environment Variables (Already Set on Render)

```
SECRET_KEY = (auto-generated)
DEBUG = False
ALLOWED_HOSTS = eduhelm-2025.onrender.com
PYTHON_VERSION = 3.11.9
ADMIN_USERNAME = admin (optional)
ADMIN_PASSWORD = Admin@2025 (optional)
```

## Common Issues

### Site returns 502 Error
- Check Render logs for errors
- Service may be starting up (wait 30-60 seconds)

### Static files not loading
- Ensure WhiteNoise is in MIDDLEWARE
- Check that `collectstatic` ran during build

### Profile photo missing
- Normal on free tier - upload after deploy
- Consider Cloudinary for persistence

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/DYNAMOatGHUB/EduHelm.2025.git
cd EduHelm.2025/project
```

2. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create admin user:
```bash
python manage.py createadmin
```

6. Run development server:
```bash
python manage.py runserver
```

7. Visit: http://127.0.0.1:8000

## Custom Domain Setup

See `CUSTOM_DOMAIN_SETUP.md` for local development custom domain instructions.

## Upgrading to Production

For a production deployment:

1. **Upgrade Render plan** ($7/month) for:
   - Always-on service (no cold starts)
   - Persistent disk for media files
   - Better performance

2. **Consider PostgreSQL** instead of SQLite:
   - Better for concurrent users
   - Render offers free PostgreSQL

3. **Add Cloudinary** for media files:
   - Free tier: 25GB storage
   - CDN delivery
   - Image transformations

4. **Set up monitoring:**
   - Sentry for error tracking
   - Google Analytics for usage

## Support

- GitHub Repo: https://github.com/DYNAMOatGHUB/EduHelm.2025
- Issues: Create an issue on GitHub


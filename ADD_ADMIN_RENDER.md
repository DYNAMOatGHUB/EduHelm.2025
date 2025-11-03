# Add Admin Credentials to Render (Free Tier Solution)

Since you can't access the Shell on Render's free tier, we've created an automatic admin user creation system that runs during deployment.

## Steps to Set Up Admin User:

### 1. Add Environment Variables to Render

Go to your Render Dashboard:
1. Click on your **EduHelm.2025** service
2. Go to **Environment** tab (left sidebar)
3. Click **Add Environment Variable**
4. Add these three variables:

```
ADMIN_USERNAME = admin
ADMIN_EMAIL = admin@eduhelm.com
ADMIN_PASSWORD = YourSecurePassword123!
```

**Important:** Change `YourSecurePassword123!` to a strong password!

### 2. Trigger a New Deployment

After adding the environment variables:
1. Go to **Manual Deploy** (top right)
2. Click **Deploy latest commit**

Or just push a new commit to trigger auto-deploy.

### 3. Admin User Will Be Created Automatically

During the build process, you'll see in the logs:
```
Creating admin user...
✅ Admin user "admin" created successfully!
```

### 4. Login to Your Site

Go to: https://eduhelm-2025.onrender.com/login

Use the credentials:
- **Username:** admin (or whatever you set in ADMIN_USERNAME)
- **Password:** (whatever you set in ADMIN_PASSWORD)

## Alternative: Use Default Credentials

If you don't set the environment variables, the system will use these defaults:
- **Username:** admin
- **Email:** admin@eduhelm.com
- **Password:** Admin@2025

⚠️ **Security Warning:** Change the default password immediately after first login!

## How It Works

The `build.sh` script now includes:
```bash
python manage.py createadmin
```

This custom Django management command:
- Checks if admin user exists
- If not, creates it using environment variables (or defaults)
- Creates the associated Profile record
- Runs automatically on every deployment (but only creates admin once)

## Next Steps After Admin is Created

1. Login to https://eduhelm-2025.onrender.com/login
2. Access admin panel: https://eduhelm-2025.onrender.com/admin
3. Change your password (recommended!)
4. Start creating courses, lessons, etc.

## Verify Admin Creation

Check the Render build logs after deployment. You should see:
```
Creating admin user...
✅ Admin user "admin" created successfully!
   Email: admin@eduhelm.com
   Password: Set from ADMIN_PASSWORD env var
```

If admin already exists, you'll see:
```
Admin user "admin" already exists
```

This means you can login with your previously set credentials.

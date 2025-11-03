# 🚀 Quick Deployment Reference Card

## Step 1: MongoDB Atlas (5 minutes)
1. Sign up: https://www.mongodb.com/cloud/atlas/register
2. Create FREE cluster (M0)
3. Create user: `eduhelm_admin` + password
4. Network Access: Allow `0.0.0.0/0`
5. Get connection string (replace <password>)
   ```
   mongodb+srv://eduhelm_admin:PASSWORD@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 2: Render (10 minutes)
1. Sign up: https://render.com/ (use GitHub login)
2. New → Web Service
3. Connect `EduHelm.2025` repo
4. Configure:
   - Name: `eduhelm`
   - Root Directory: `project`
   - Build: `./build.sh`
   - Start: `gunicorn project_1.wsgi:application`
   - Free tier

## Step 3: Environment Variables
Add in Render dashboard:
```
SECRET_KEY = [generate new at https://djecrety.ir/]
DEBUG = False
ALLOWED_HOSTS = your-app-name.onrender.com
MONGODB_URI = mongodb+srv://eduhelm_admin:PASSWORD@cluster...
MONGODB_NAME = eduhelm_db
PYTHON_VERSION = 3.11.9
```

## Step 4: Deploy & Create Admin
1. Click "Create Web Service" (wait 5-10 min)
2. Open Shell tab
3. Run:
   ```bash
   cd project
   python manage.py createsuperuser
   ```

## Your Live Site
- URL: `https://your-name.onrender.com`
- Admin: `https://your-name.onrender.com/admin/`

## Push Changes to GitHub First
```bash
git push origin main
```

## Full Guide
See: DEPLOYMENT_GUIDE.md

## Estimated Time
- Total: 20-30 minutes
- Cost: $0/month (FREE tier)

✅ Ready to deploy!

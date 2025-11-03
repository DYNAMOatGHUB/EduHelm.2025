# 🚀 EduHelm Deployment Guide
## Deploy to Render with MongoDB Atlas (FREE)

**Total Cost: $0/month**  
**Time Required: 20-30 minutes**  
**Your Site URL: `https://your-app-name.onrender.com`**

---

## 📋 Prerequisites

- ✅ GitHub account (you have this)
- ✅ Code pushed to GitHub (done: https://github.com/DYNAMOatGHUB/EduHelm.2025)
- 🆕 MongoDB Atlas account (we'll create this)
- 🆕 Render account (we'll create this)

---

## PART 1: Setup MongoDB Atlas (Cloud Database) ☁️

### Step 1: Create MongoDB Atlas Account

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up with:
   - Email address
   - OR use Google/GitHub login
3. Choose **FREE tier** (M0 Sandbox)

### Step 2: Create a Cluster

1. After login, click **"Build a Database"**
2. Choose **FREE** tier (M0 - 512 MB storage)
3. Choose **Cloud Provider**: AWS
4. Choose **Region**: Select closest to you or your users
   - Example: `us-east-1` (Virginia) for USA
   - Example: `ap-south-1` (Mumbai) for India
5. **Cluster Name**: `eduhelm-cluster` (or any name)
6. Click **"Create Cluster"** (takes 1-3 minutes)

### Step 3: Create Database User

1. Click **"Database Access"** in left sidebar
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Set:
   - Username: `eduhelm_admin` (remember this!)
   - Password: Click **"Autogenerate Secure Password"** (COPY THIS!)
   - OR create your own strong password
5. **User Privileges**: Select **"Read and write to any database"**
6. Click **"Add User"**

**⚠️ IMPORTANT: Save your password now! You won't see it again.**

### Step 4: Allow Network Access

1. Click **"Network Access"** in left sidebar
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for Render deployment)
   - IP: `0.0.0.0/0`
   - Description: `Render deployment`
4. Click **"Confirm"**

### Step 5: Get Connection String

1. Click **"Database"** in left sidebar
2. Click **"Connect"** on your cluster
3. Click **"Connect your application"**
4. **Driver**: Python, **Version**: 3.12 or later
5. **Copy the connection string** - looks like:
   ```
   mongodb+srv://eduhelm_admin:<password>@eduhelm-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **Replace `<password>`** with your actual password from Step 3
7. **Save this complete URI** - you'll need it for Render!

**Example final URI:**
```
mongodb+srv://eduhelm_admin:MySecurePass123@eduhelm-cluster.abc12.mongodb.net/?retryWrites=true&w=majority
```

---

## PART 2: Deploy to Render 🎯

### Step 1: Create Render Account

1. Go to: https://render.com/
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest - auto-connects your repos)
4. Authorize Render to access your GitHub

### Step 2: Create New Web Service

1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your repository:
   - If not connected, click **"Configure account"** → Allow access to `EduHelm.2025` repo
4. Select **`EduHelm.2025`** repository
5. Click **"Connect"**

### Step 3: Configure Web Service

Fill in the deployment settings:

**Basic Settings:**
- **Name**: `eduhelm` (this becomes your URL: eduhelm.onrender.com)
- **Region**: Choose closest to you (e.g., Oregon USA, Frankfurt EU, Singapore Asia)
- **Branch**: `main`
- **Root Directory**: `project` ⚠️ IMPORTANT - your Django project is in this folder
- **Runtime**: `Python 3`

**Build & Deploy Settings:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn project_1.wsgi:application`

**Instance Type:**
- Select **"Free"** (0$/month) ✅

### Step 4: Set Environment Variables

Scroll down to **"Environment Variables"** section and add these:

Click **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate new: https://djecrety.ir/ (click "Generate") |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `eduhelm.onrender.com` (replace with your actual service name) |
| `MONGODB_URI` | `mongodb+srv://eduhelm_admin:YourPassword@eduhelm-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority` |
| `MONGODB_NAME` | `eduhelm_db` |
| `PYTHON_VERSION` | `3.11.9` |

**⚠️ Replace these with YOUR actual values:**
- Use YOUR MongoDB connection string from Part 1, Step 5
- Use YOUR Render service name in ALLOWED_HOSTS
- Generate a NEW SECRET_KEY (don't use the one from local development)

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render will start building your app (takes 5-10 minutes first time)
3. Watch the logs - you'll see:
   - Installing dependencies
   - Collecting static files
   - Starting server

### Step 6: Wait for Deployment

**Build logs will show:**
```
==> Installing dependencies from requirements.txt
==> Running build command: ./build.sh
Collecting static files...
Build completed successfully!
==> Starting server: gunicorn project_1.wsgi:application
Your service is live 🎉
```

**When you see "Your service is live"** - deployment is complete!

---

## PART 3: Create Admin User & Test 🧪

### Step 1: Access Render Shell

1. In Render dashboard, click on your **"eduhelm"** service
2. Click **"Shell"** tab (top right)
3. Wait for shell to connect

### Step 2: Create Superuser

In the Render shell, run:

```bash
cd project
python manage.py createsuperuser
```

Follow prompts:
- Username: `admin`
- Email: `your-email@example.com`
- Password: (choose a strong password)
- Password (again): (confirm)

### Step 3: Test Your Site!

1. Visit your site: `https://eduhelm.onrender.com` (use YOUR service name)
2. Test pages:
   - ✅ Homepage: `https://eduhelm.onrender.com/`
   - ✅ Register: `https://eduhelm.onrender.com/register/`
   - ✅ Login: `https://eduhelm.onrender.com/login/`
   - ✅ Admin: `https://eduhelm.onrender.com/admin/`

3. Create a test account and try features:
   - Register new user
   - Login
   - View dashboard
   - Start study session
   - Create note

---

## 🎨 Upload Media Files (Profile Pictures)

**For production, you should use cloud storage (S3/Cloudinary) for user uploads.**

**Quick fix for now (Render free tier):**

⚠️ **Note**: Render free tier **doesn't persist media files** between deploys.  
For production, integrate:
- **Cloudinary** (free tier: 25GB/month) - Recommended
- **AWS S3** (paid but cheap)

**To add Cloudinary (optional for now):**

1. Sign up: https://cloudinary.com/users/register_free
2. Get your credentials
3. Install: Add `cloudinary` and `django-cloudinary-storage` to `requirements.txt`
4. Configure in `settings.py`

**For now:** Test without profile pictures, or accept they'll reset on redeploy.

---

## ⚙️ Troubleshooting

### Issue: "Application failed to start"

**Solution 1:** Check Build Logs
- In Render dashboard → Click your service → "Logs" tab
- Look for error messages

**Solution 2:** Verify Environment Variables
- Check all variables are set correctly
- MongoDB URI has your actual password
- ALLOWED_HOSTS includes your Render URL

**Solution 3:** Check Build Command
- Root Directory should be `project`
- Build command: `./build.sh`
- Start command: `gunicorn project_1.wsgi:application`

### Issue: "502 Bad Gateway"

- Service is deploying (wait 5-10 min)
- OR build failed (check logs)

### Issue: "MongoDB connection failed"

**Check:**
1. MongoDB Atlas cluster is running
2. Network Access allows `0.0.0.0/0`
3. Database user exists with correct password
4. MONGODB_URI in Render is correct (no spaces, password is correct)

**Test MongoDB URI:**
In Render shell:
```bash
python
>>> from pymongo import MongoClient
>>> client = MongoClient('your-mongodb-uri-here')
>>> client.server_info()
# Should return server details if connection works
```

### Issue: "Static files not loading (no CSS)"

**Solution:**
```bash
# In Render shell
cd project
python manage.py collectstatic --no-input
```

Then restart the service.

### Issue: "Admin user can't login"

**Recreate admin:**
```bash
# In Render shell
cd project
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@eduhelm.com', 'YourNewPassword123')
exit()
```

---

## 🔄 Deploying Updates

**After making changes locally:**

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. **Render auto-deploys** (if you enabled auto-deploy)
   - OR manually deploy: Render Dashboard → Your service → "Manual Deploy" → "Deploy latest commit"

3. **Wait 3-5 minutes** for deployment

4. **Test changes** at your live URL

---

## 📊 Monitor Your Site

### Render Dashboard Shows:

- **Metrics**: CPU, Memory, Request count
- **Logs**: Real-time application logs
- **Events**: Deployment history
- **Shell**: Access to your server

### MongoDB Atlas Dashboard Shows:

- **Database size**: Current usage
- **Connections**: Active connections
- **Performance**: Query performance

---

## 💰 Cost Breakdown

| Service | Tier | Cost |
|---------|------|------|
| Render Web Service | Free | $0/month |
| MongoDB Atlas | M0 (512MB) | $0/month |
| **TOTAL** | | **$0/month** ✅ |

### Free Tier Limitations:

**Render Free:**
- ✅ Good for: Portfolio, demos, small projects
- ⚠️ Spins down after 15 min inactivity (first request slow)
- ⚠️ No persistent disk (media files reset on deploy)
- ⚠️ 750 hours/month limit (enough for one site 24/7)

**MongoDB Atlas Free:**
- ✅ 512 MB storage (good for thousands of users)
- ✅ Shared cluster
- ✅ Good for: Small to medium apps

### Upgrade When Needed:

**Render Paid ($7/month):**
- Always running (no spin-down)
- Persistent disk
- More memory/CPU

**MongoDB Atlas Paid ($9/month):**
- Dedicated cluster
- More storage
- Better performance

---

## 🎉 Success Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with password
- [ ] Network access configured (0.0.0.0/0)
- [ ] MongoDB connection string copied
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Environment variables set in Render
- [ ] First deployment successful
- [ ] Site accessible at: https://your-name.onrender.com
- [ ] Admin user created
- [ ] Login/Register working
- [ ] Features tested (study, notes, courses)

---

## 🔗 Quick Links

**Your Resources:**
- **Live Site**: `https://eduhelm.onrender.com` (replace with yours)
- **Render Dashboard**: https://dashboard.render.com/
- **MongoDB Atlas**: https://cloud.mongodb.com/
- **GitHub Repo**: https://github.com/DYNAMOatGHUB/EduHelm.2025

**Support:**
- Render Docs: https://render.com/docs
- MongoDB Docs: https://www.mongodb.com/docs/atlas/
- Django Deployment: https://docs.djangoproject.com/en/3.1/howto/deployment/

---

## 📝 Notes

1. **First load is slow**: Render free tier spins down after 15 min inactivity. First request wakes it up (30-60 seconds).

2. **Media files**: For production, use Cloudinary or S3 for uploads (profile pics, resources).

3. **Database backups**: MongoDB Atlas free tier doesn't include automated backups. Export your data manually if critical.

4. **Custom domain**: Upgrade to Render paid plan to use your own domain (e.g., eduhelm.com).

5. **HTTPS**: Render provides free SSL/HTTPS automatically ✅

---

## 🚀 You're Live!

**Congratulations!** Your EduHelm platform is now deployed and accessible worldwide! 🌍

**Share your live URL:**
- Portfolio: Add to resume/portfolio
- Demo: Share with potential employers
- Feedback: Share with friends for testing

**Next Steps:**
- [ ] Share URL with team/friends
- [ ] Collect feedback
- [ ] Monitor usage in dashboards
- [ ] Plan future features (AI mentor!)

---

*Created: November 3, 2025*  
*For: EduHelm Educational Platform*  
*Deployment: Render + MongoDB Atlas (Free Tier)*

# PostgreSQL Setup Guide for EduHelm

## 🎯 Why PostgreSQL?

Your project now uses **PostgreSQL** for production to ensure:
- ✅ **Persistent Data** - User accounts survive deployments
- ✅ **Production Ready** - Industry standard database
- ✅ **Free Tier Available** - Render offers free PostgreSQL
- ✅ **Scalable** - Handles thousands of users

---

## 📋 What Changed?

### 1. **requirements.txt** - Added PostgreSQL packages
```
psycopg2-binary==2.9.9  # PostgreSQL adapter for Python
dj-database-url==0.5.0  # Parse database URLs
```

### 2. **settings.py** - Smart database configuration
```python
# Automatically detects environment:
# - Production (Render) → PostgreSQL
# - Local Development → SQLite
if config('DATABASE_URL', default=None):
    DATABASES = {'default': dj_database_url.config(...)}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', ...}}
```

---

## 🚀 Render Deployment Steps

### Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +"** → Select **"PostgreSQL"**
3. **Configure Database**:
   - **Name**: `eduhelm-database` (or any name you prefer)
   - **Database**: `eduhelm_db`
   - **User**: `eduhelm_user` (auto-generated)
   - **Region**: Choose closest to your web service
   - **Plan**: **Free** (90 days free, then $7/month)
4. **Click "Create Database"**
5. **Wait 2-3 minutes** for database to be created

### Step 2: Copy Database URL

1. After database is created, you'll see an **"Info"** tab
2. Find **"Internal Database URL"** (looks like this):
   ```
   postgresql://eduhelm_user:LONG_PASSWORD_HERE@dpg-xyz123.oregon-postgres.render.com/eduhelm_db
   ```
3. **Copy this entire URL** - you'll need it in the next step

### Step 3: Add Database URL to Web Service

1. Go to your **Web Service** dashboard (your Django app)
2. Click **"Environment"** tab on the left
3. Click **"Add Environment Variable"**
4. Add the following:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL you copied
5. **Click "Save Changes"**

### Step 4: Deploy Your Changes

**Option A: Auto-deploy (if enabled)**
```bash
# Just push your code to GitHub
git add .
git commit -m "Add PostgreSQL support for persistent data"
git push origin main
```
Render will automatically deploy!

**Option B: Manual deploy**
1. Go to Render dashboard → Your web service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🔍 Verify It's Working

### 1. Check Deployment Logs
```
Installing dependencies...
✓ psycopg2-binary installed
Running migrations...
✓ Applying migrations to PostgreSQL
Build completed successfully!
```

### 2. Test User Registration
1. Go to your deployed site: `https://your-app.onrender.com/register/`
2. Create a test account
3. Deploy a new update (any small change)
4. Try logging in → **Account should still exist!** ✅

---

## 🧪 Local Development

Your local development is **unaffected**! It still uses SQLite:

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run migrations (SQLite locally)
python manage.py migrate

# Create local admin
python manage.py createsuperuser

# Run server
python manage.py runserver
```

**Why?** Settings.py detects no `DATABASE_URL` environment variable, so it uses SQLite.

---

## 🔧 Environment Variables Summary

### Required on Render:
```
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
```

### Optional (Already set):
```
DJANGO_SETTINGS_MODULE=project_1.settings
PYTHON_VERSION=3.11.9
```

---

## 📊 Database Migration Commands

### On Render (Automatic in build.sh):
```bash
python manage.py migrate  # Runs on PostgreSQL
```

### Locally (Manual):
```bash
python manage.py migrate  # Runs on SQLite
python manage.py createsuperuser  # Create admin locally
```

---

## 🚨 Troubleshooting

### Error: "no such table: auth_user"
**Solution**: Migrations didn't run. Check build.sh includes:
```bash
python manage.py migrate
```

### Error: "connection refused"
**Solution**: DATABASE_URL is incorrect. Check:
1. Copied the **Internal Database URL** (not External)
2. URL is complete (starts with `postgresql://`)
3. No extra spaces in environment variable

### Error: "psycopg2 not installed"
**Solution**: 
1. Check `requirements.txt` includes `psycopg2-binary==2.9.9`
2. Redeploy to reinstall dependencies

### Database is Empty After Deploy
**Solution**: This is normal for first deployment!
1. Go to your site's `/register/` page
2. Create your first user account
3. User data will now persist across deployments

---

## 💾 Data Persistence Examples

### Before PostgreSQL (SQLite):
```
Day 1: User registers → Saved to db.sqlite3
Day 2: You deploy update → db.sqlite3 DELETED ❌
Day 2: User tries to login → Account not found ❌
```

### After PostgreSQL:
```
Day 1: User registers → Saved to PostgreSQL ✅
Day 2: You deploy update → PostgreSQL untouched ✅
Day 2: User tries to login → Account found! ✅
Day 100: User logins → Still works! ✅
```

---

## 📈 PostgreSQL Free Tier Limits

| Feature | Free Tier | Paid Tier ($7/mo) |
|---------|-----------|-------------------|
| Storage | 1 GB | 10 GB - 500 GB |
| Duration | 90 days free | Unlimited |
| Connections | 97 | 97 - 500 |
| Backups | Daily (7 days) | Daily (14 days) |
| RAM | 1 GB | 1 GB - 512 GB |

**Perfect for**: Personal projects, portfolios, small apps with <1000 users

---

## ✅ Post-Setup Checklist

- [ ] PostgreSQL database created on Render
- [ ] `DATABASE_URL` added to web service environment variables
- [ ] Code pushed to GitHub
- [ ] Render deployed successfully
- [ ] Can register a new user
- [ ] User can login after registration
- [ ] Deploy a test update
- [ ] User can still login (data persisted!) ✅

---

## 🎉 You're All Set!

Your EduHelm project now has:
- **Persistent database** - User data survives deployments
- **Production-ready** - PostgreSQL is industry standard
- **Auto-detection** - Uses PostgreSQL on Render, SQLite locally
- **Future-proof** - Can scale to thousands of users

**Next Steps**:
1. Follow the deployment steps above
2. Test user registration
3. Deploy an update to verify data persistence
4. Start building features knowing user data is safe! 🚀

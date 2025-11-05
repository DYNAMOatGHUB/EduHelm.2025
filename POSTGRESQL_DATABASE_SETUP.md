# PostgreSQL Database Setup on Render

## 🚀 Step 1: Create PostgreSQL Database on Render

### A. Create New PostgreSQL Instance

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +"** → Select **"PostgreSQL"**
3. **Configure Database**:
   ```
   Name: eduhelm-db
   Database: eduhelm_db
   User: eduhelm_user
   Region: Oregon (US West) or closest to you
   PostgreSQL Version: 16
   Plan: Free
   ```
4. **Click "Create Database"**
5. **Wait 2-3 minutes** for database to be created

### B. Get Database Connection Details

After creation, you'll see:
```
Internal Database URL: postgresql://eduhelm_user:xxxxx@dpg-xxxxx/eduhelm_db
External Database URL: postgresql://eduhelm_user:xxxxx@dpg-xxxxx-a.oregon-postgres.render.com/eduhelm_db
POSTGRES_HOST: dpg-xxxxx-a.oregon-postgres.render.com
POSTGRES_DATABASE: eduhelm_db
POSTGRES_USER: eduhelm_user
POSTGRES_PASSWORD: xxxxxxxxxxxxx
POSTGRES_PORT: 5432
```

**⚠️ IMPORTANT**: Copy the **Internal Database URL** - you'll need this!

---

## 🔧 Step 2: Connect Your Web Service to PostgreSQL

### A. Add Environment Variable to Web Service

1. **Go to your Web Service** (eduhelm or whatever you named it)
2. **Click "Environment"** tab on the left
3. **Add New Environment Variable**:
   ```
   Key: DATABASE_URL
   Value: [Paste the Internal Database URL from Step 1B]
   ```
   Example:
   ```
   DATABASE_URL=postgresql://eduhelm_user:longpassword123@dpg-xxxxx/eduhelm_db
   ```
4. **Click "Save Changes"**

### B. Redeploy

Your web service will **automatically redeploy** with the new database connection.

**Wait for deployment to complete** (check the "Logs" tab).

---

## 🎛️ Step 3: Access Your PostgreSQL Database

### **Method 1: Render Dashboard (Web Interface)** ⭐ EASIEST

1. Go to your **PostgreSQL database** in Render dashboard
2. Click **"Connect"** button (top right)
3. Click **"External Connection"** tab
4. Use these credentials with any tool you like

### **Method 2: Django Admin Panel** ⭐ RECOMMENDED

**Access your production admin panel:**

1. **URL**: `https://your-app.onrender.com/admin/`
2. **Login**: Use the admin credentials that were created during deployment
   - Default username: `admin`
   - Check your deployment logs for the auto-generated password
   - Or reset using method below

**What You Can Do:**
- ✅ View all users
- ✅ Edit user data
- ✅ Delete users
- ✅ View all courses, schedules, tasks, notes
- ✅ Manage all database tables

**Admin Permissions:**
- ✅ Full access to entire database
- ✅ Can add/edit/delete any data
- ✅ Can make other users admins

**Regular User Permissions:**
- ✅ Can only see/edit their own data
- ❌ Cannot see other users' data
- ❌ Cannot access admin panel

### **Method 3: pgAdmin (Desktop App)** 🖥️

**Download pgAdmin**: https://www.pgadmin.org/download/

**Connect to Database:**
1. Open pgAdmin
2. Right-click **"Servers"** → **"Register"** → **"Server"**
3. **General Tab**:
   ```
   Name: EduHelm Production DB
   ```
4. **Connection Tab**:
   ```
   Host: [POSTGRES_HOST from Render]
   Port: 5432
   Database: eduhelm_db
   Username: [POSTGRES_USER from Render]
   Password: [POSTGRES_PASSWORD from Render]
   ```
5. Click **"Save"**

**Now you can:**
- ✅ Browse all tables
- ✅ Run SQL queries
- ✅ Export data
- ✅ View user data
- ✅ Create backups

### **Method 4: DBeaver (Free Database Tool)** 🛠️

**Download DBeaver**: https://dbeaver.io/download/

**Connect:**
1. Click **"New Database Connection"**
2. Select **"PostgreSQL"**
3. Enter connection details from Render
4. Click **"Test Connection"** → **"Finish"**

### **Method 5: Command Line (psql)** 💻

**From your terminal:**
```bash
psql [External Database URL from Render]
```

Example:
```bash
psql postgresql://eduhelm_user:password@dpg-xxxxx-a.oregon-postgres.render.com/eduhelm_db
```

**Useful SQL Commands:**
```sql
-- View all users
SELECT * FROM auth_user;

-- Count total users
SELECT COUNT(*) FROM auth_user;

-- View user profiles
SELECT * FROM users_profile;

-- View all tables
\dt

-- Exit
\q
```

---

## 🔐 Step 4: Reset Admin Password (If Needed)

If you need to create/reset the admin account:

### A. Using Render Shell

1. **Go to your Web Service** in Render dashboard
2. Click **"Shell"** tab on the left
3. Run these commands:
   ```bash
   cd project
   python manage.py createsuperuser
   ```
4. Follow the prompts:
   ```
   Username: admin
   Email: your-email@example.com
   Password: [enter secure password]
   Password (again): [confirm password]
   ```

### B. Using Custom Command

The `createadmin` command already runs during deployment, but to reset:

1. **SSH into Render Shell** (from dashboard)
2. Run:
   ```bash
   cd project
   python manage.py shell
   ```
3. In Python shell:
   ```python
   from django.contrib.auth.models import User
   user = User.objects.get(username='admin')
   user.set_password('your-new-password')
   user.save()
   exit()
   ```

---

## 📊 Database Tables Overview

Your PostgreSQL database contains these tables:

### **Django System Tables:**
- `auth_user` - User accounts (username, email, password)
- `auth_group` - User groups
- `auth_permission` - Permissions system
- `django_session` - Login sessions
- `django_admin_log` - Admin activity log

### **Your App Tables:**
- `users_profile` - User profiles (bio, image, etc.)
- `users_studyschedule` - Study schedules
- `schedule_task` - User tasks
- `courses_course` - Courses
- `courses_lesson` - Lessons
- `courses_enrollment` - User course enrollments

### **Example Queries:**

```sql
-- View all registered users
SELECT id, username, email, date_joined, is_active 
FROM auth_user 
ORDER BY date_joined DESC;

-- Count users by registration date
SELECT DATE(date_joined) as date, COUNT(*) as users 
FROM auth_user 
GROUP BY DATE(date_joined);

-- View user profiles with user info
SELECT u.username, u.email, p.bio, p.image 
FROM auth_user u 
LEFT JOIN users_profile p ON u.id = p.user_id;

-- View all tasks
SELECT t.*, u.username 
FROM schedule_task t 
JOIN auth_user u ON t.user_id = u.id;
```

---

## 🔄 Data Persistence Verification

### Test That Data Persists:

1. **Register a test user** on your deployed site
2. **Redeploy your web service** (Manual Deploy)
3. **Try logging in** with the same user
4. **✅ If login works** → Database is persistent!
5. **❌ If login fails** → Check DATABASE_URL environment variable

---

## 🛡️ Security Best Practices

### Admin Access:
1. ✅ **Use strong passwords** (16+ characters, mixed case, numbers, symbols)
2. ✅ **Change default admin password** immediately
3. ✅ **Don't share admin credentials**
4. ✅ **Use environment variables** for sensitive data
5. ✅ **Enable 2FA on Render account**

### Database Security:
1. ✅ **Use Internal Database URL** in production (faster, more secure)
2. ✅ **Never commit DATABASE_URL** to git
3. ✅ **Use External URL** only for admin access from your computer
4. ✅ **Regularly backup database** (Render does this automatically)
5. ✅ **Monitor database usage** (Render free tier: 1GB storage, 97 hours/month)

---

## 📦 Database Backup

### Manual Backup (Download):

**Method 1: Using Render Dashboard**
1. Go to PostgreSQL database in Render
2. Click **"Backups"** tab
3. Click **"Create Backup"**
4. Download backup file

**Method 2: Using pg_dump**
```bash
pg_dump [External Database URL] > backup.sql
```

**Restore from backup:**
```bash
psql [External Database URL] < backup.sql
```

---

## 📈 Monitoring Database

### Check Database Size:

**In psql:**
```sql
SELECT pg_size_pretty(pg_database_size('eduhelm_db'));
```

### Check Table Sizes:
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### View Active Connections:
```sql
SELECT * FROM pg_stat_activity;
```

---

## 🆘 Troubleshooting

### Issue: "Database connection failed"
**Solution:**
- Check DATABASE_URL in environment variables
- Verify PostgreSQL database is running (green status in Render)
- Use **Internal Database URL** not External

### Issue: "No such table: auth_user"
**Solution:**
- Run migrations: `python manage.py migrate`
- Check deployment logs - migrations should run automatically via `build.sh`

### Issue: "Can't login to admin panel"
**Solution:**
- Reset password using Render Shell
- Verify admin user exists: `python manage.py shell` → `User.objects.filter(is_superuser=True)`

### Issue: "Data disappeared after deployment"
**Solution:**
- Check if DATABASE_URL environment variable is set
- Verify you're using PostgreSQL not SQLite
- Check database connection in Django shell

---

## ✅ Verification Checklist

- [ ] PostgreSQL database created on Render
- [ ] DATABASE_URL added to web service environment variables
- [ ] Web service redeployed successfully
- [ ] Can access admin panel at `/admin/`
- [ ] Can register new user on deployed site
- [ ] User data persists after redeployment
- [ ] Can view users in admin panel
- [ ] Database accessible via pgAdmin/DBeaver
- [ ] Admin password is secure and changed from default

---

## 🎯 Quick Start Commands

```bash
# Connect to production database
psql [External Database URL]

# View all users
SELECT * FROM auth_user;

# Create backup
pg_dump [External Database URL] > backup_$(date +%Y%m%d).sql

# Reset admin password (in Django shell on Render)
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.set_password('new_secure_password')
user.save()
```

---

## 📞 Support

- **Render Documentation**: https://render.com/docs/databases
- **Django Admin Docs**: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Your production database is now set up! Users can register and their data will persist permanently.** 🎉

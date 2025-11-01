# 🌐 EduHelm Custom Domain Setup

## ✨ Access EduHelm with Beautiful URL

Instead of: `http://127.0.0.1:8000`  
Use: **`http://eduhelm.local:8000`** 🎉

---

## 🚀 Quick Setup (One-Time Only)

### **Step 1: Run Setup Script as Administrator**

1. **Right-click** on `Setup-CustomDomain.ps1`
2. Select **"Run with PowerShell"**
3. If prompted, click **"Yes"** to allow Administrator access
4. Script will add `eduhelm.local` to your Windows hosts file

### **Step 2: Start Your Server**

Run server manually:
```powershell
cd project
python manage.py runserver
```

### **Step 3: Access EduHelm**

Open your browser and go to:
```
http://eduhelm.local:8000
```

**Bookmark it!** 🔖

---

## 📱 Available URLs

After setup, you can use any of these:

✅ **Custom Domain (Recommended):**
- `http://eduhelm.local:8000`
- `http://www.eduhelm.local:8000`

✅ **Standard URLs (Still Work):**
- `http://127.0.0.1:8000`
- `http://localhost:8000`

---

## 🛠️ Manual Setup (If Script Doesn't Work)

### **Option A: Edit Hosts File Manually**

1. Press `Win + R`
2. Type: `notepad C:\Windows\System32\drivers\etc\hosts`
3. Click **"Run as Administrator"**
4. Add these lines at the end:
   ```
   127.0.0.1       eduhelm.local
   127.0.0.1       www.eduhelm.local
   ```
5. Save and close

### **Option B: Use PowerShell Command**

Run PowerShell **as Administrator** and paste:

```powershell
Add-Content -Path "C:\Windows\System32\drivers\etc\hosts" -Value "`n127.0.0.1       eduhelm.local`n127.0.0.1       www.eduhelm.local"
```

---

## ❓ Troubleshooting

### **"eduhelm.local" Not Working?**

1. **Flush DNS Cache:**
   ```powershell
   ipconfig /flushdns
   ```

2. **Restart Browser** (close completely and reopen)

3. **Check Hosts File:**
   - Open: `C:\Windows\System32\drivers\etc\hosts`
   - Verify these lines exist:
     ```
     127.0.0.1       eduhelm.local
     127.0.0.1       www.eduhelm.local
     ```

4. **Try Different Browser** (Chrome, Firefox, Edge)

### **Still See "This site can't be reached"?**

- Make sure Django server is **running**
- Check server shows: `Starting development server at http://127.0.0.1:8000/`

---

## 🎯 Remove Custom Domain (If Needed)

1. Open: `C:\Windows\System32\drivers\etc\hosts` as Administrator
2. Delete these lines:
   ```
   127.0.0.1       eduhelm.local
   127.0.0.1       www.eduhelm.local
   ```
3. Save file
4. Run: `ipconfig /flushdns`

---

## 🎉 Enjoy Your Custom Domain!

Now you can access EduHelm with a professional-looking URL:

**`http://eduhelm.local:8000`** 

Much better than `http://127.0.0.1:8000`! 🚀

*Last Updated: November 1, 2025*

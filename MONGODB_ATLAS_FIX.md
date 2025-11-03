# MongoDB Atlas Connection Fix for Djongo

## Problem
Djongo 1.3.7 with pymongo 3.11.4 has SSL/TLS handshake issues with modern MongoDB Atlas clusters.

Error: `SSL handshake failed: [SSL: TLSV1_ALERT_INTERNAL_ERROR]`

## Solution

### Update Your MongoDB Atlas Connection String in Render

1. Go to Render Dashboard → EduHelm.2025 → **Environment** tab
2. Find the `MONGODB_URI` variable
3. Add `&tlsAllowInvalidCertificates=true` to the end of your connection string

**Before:**
```
mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

**After:**
```
mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true
```

4. Click "Save Changes"
5. Trigger a manual deploy

### Alternative: Update MongoDB Atlas TLS/SSL Settings

If the above doesn't work, try:

1. In Render environment variables, modify `MONGODB_URI` to:
```
mongodb+srv://username:password@cluster.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=false
```

### Why This Happens

- MongoDB Atlas uses modern TLS 1.2/1.3
- pymongo 3.11.4 (required by djongo 1.3.7) has limited SSL support
- Older Python SSL libraries on some systems can't negotiate the handshake
- Allowing invalid certificates bypasses strict verification while maintaining encryption

### Security Note

⚠️ `tlsAllowInvalidCertificates=true` reduces security slightly but:
- Connection is still encrypted
- Only bypasses certificate validation
- Required for djongo compatibility
- Alternative is to migrate away from djongo (requires major refactoring)

### Long-term Solution

Consider migrating to:
- Django 4.x or 5.x with native MongoDB support (djongo-next or direct pymongo)
- PostgreSQL or MySQL with Django's native ORM
- Direct pymongo usage without Django ORM (more work)

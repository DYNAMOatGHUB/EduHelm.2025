import pymongo
import django
import os
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.conf import settings

print('╔══════════════════════════════════════════════════════════════╗')
print('║          MONGODB DATABASE CONNECTION REPORT                 ║')
print('╚══════════════════════════════════════════════════════════════╝')
print()

# MongoDB Connection
client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)

# Test Connection
try:
    client.admin.command('ping')
    print('✅ MongoDB Server: ONLINE & CONNECTED')
except Exception as e:
    print(f'❌ MongoDB Server: CONNECTION FAILED - {e}')
    sys.exit(1)

print(f'📍 Server Address: {client.address[0]}:{client.address[1]}')
print(f'🔌 Connection String: mongodb://localhost:27017/')
print()

# Django Settings
print('⚙️  DJANGO DATABASE CONFIGURATION:')
print('─' * 65)
db_config = settings.DATABASES['default']
print(f'  Engine: {db_config["ENGINE"]}')
print(f'  Database Name: {db_config["NAME"]}')
print(f'  Host: {db_config["CLIENT"]["host"]}')
print(f'  Port: {db_config["CLIENT"]["port"]}')
print(f'  Enforce Schema: {db_config["ENFORCE_SCHEMA"]}')
print()

# Database Info
db = client[db_config['NAME']]
collections = sorted(db.list_collection_names())

print(f'📊 DATABASE: {db_config["NAME"]}')
print('─' * 65)
print(f'  Total Collections: {len(collections)}')
print()

if len(collections) == 0:
    print('  ⚠️  WARNING: No collections found!')
    print('  💡 Run: python setup_surprise_features.py')
else:
    print('  📚 ALL COLLECTIONS:')
    
    # Group collections by app
    django_core = []
    users_app = []
    courses_app = []
    other = []
    
    for col in collections:
        if col.startswith('auth_') or col.startswith('django_') or col.startswith('admin_'):
            django_core.append(col)
        elif col.startswith('users_'):
            users_app.append(col)
        elif col.startswith('courses_'):
            courses_app.append(col)
        else:
            other.append(col)
    
    if django_core:
        print(f'\n  🔐 Django Core ({len(django_core)}):')
        for col in django_core:
            count = db[col].count_documents({})
            print(f'     • {col:45} - {count:5} docs')
    
    if users_app:
        print(f'\n  👤 Users App ({len(users_app)}):')
        for col in users_app:
            count = db[col].count_documents({})
            emoji = '🏆' if 'badge' in col else '🔔' if 'notification' in col else '📊' if 'activity' in col else '📝'
            print(f'     {emoji} {col:45} - {count:5} docs')
    
    if courses_app:
        print(f'\n  🎓 Courses App ({len(courses_app)}):')
        for col in courses_app:
            count = db[col].count_documents({})
            print(f'     • {col:45} - {count:5} docs')
    
    if other:
        print(f'\n  📦 Other ({len(other)}):')
        for col in other:
            count = db[col].count_documents({})
            print(f'     • {col:45} - {count:5} docs')

print()
print('✅ CONNECTION STATUS SUMMARY:')
print('─' * 65)
print('  • MongoDB Server: ✅ Running')
print('  • Django Connection: ✅ Configured')
print(f'  • Database "{db_config["NAME"]}": ✅ Connected')
print(f'  • Collections: ✅ {len(collections)} found')
print('─' * 65)

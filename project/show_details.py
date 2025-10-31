import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['eduhelm_db']

print('\n' + '='*70)
print('🔔 NOTIFICATIONS CREATED')
print('='*70)

notifs = list(db.users_notification.find())
for i, n in enumerate(notifs, 1):
    print(f'\n{i}. {n["title"]}')
    print(f'   Type: {n["notification_type"]}')
    print(f'   User ID: {n["user_id"]}')
    print(f'   Message: {n["message"]}')
    print(f'   Read: {n["is_read"]}')

print('\n' + '='*70)
print('🏆 ALL 13 BADGES')
print('='*70)

badges = list(db.users_badge.find())
for i, b in enumerate(badges, 1):
    print(f'\n{i:2}. {b["name"]:30} [{b["badge_type"]:8}]')
    print(f'    Icon: {b["icon"]:20} Color: {b["color"]}')
    print(f'    Requirement: {b["requirement"]:3} | {b["description"]}')

print('\n' + '='*70)
print('📊 SUMMARY')
print('='*70)
print(f'✅ Badges Created: {len(badges)}')
print(f'✅ Notifications Created: {len(notifs)}')
print(f'✅ User Badges Earned: {db.users_userbadge.count_documents({})}')
print(f'✅ Activities Logged: {db.users_useractivity.count_documents({})}')
print('='*70)

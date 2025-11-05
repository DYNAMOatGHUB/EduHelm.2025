"""
Management command to reset admin password
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Resets admin user password'

    def handle(self, *args, **options):
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'EduHelm@Admin2025')

        try:
            # Get the admin user
            admin = User.objects.get(username=admin_username)
            
            # Reset password
            admin.set_password(admin_password)
            admin.save()

            # Show success message
            password_display = admin_password if not os.environ.get('ADMIN_PASSWORD') else "Set from ADMIN_PASSWORD env var"
            self.stdout.write(self.style.SUCCESS(
                f'\n{"="*60}\n'
                f'✅ ADMIN PASSWORD RESET SUCCESSFULLY!\n'
                f'{"="*60}\n'
                f'📌 New admin credentials:\n'
                f'   Username: {admin_username}\n'
                f'   Password: {password_display}\n'
                f'{"="*60}\n'
                f'⚠️  IMPORTANT: Change this password after first login!\n'
                f'{"="*60}\n'
            ))

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'❌ Admin user "{admin_username}" does not exist!\n'
                f'   Run: python manage.py createadmin'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error resetting password: {str(e)}'))

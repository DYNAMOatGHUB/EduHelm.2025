"""
Management command to create admin user if it doesn't exist
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile
import os


class Command(BaseCommand):
    help = 'Creates admin user if it does not exist'

    def handle(self, *args, **options):
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@eduhelm.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'EduHelm@Admin2025')

        # Check if admin exists
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(self.style.WARNING(f'Admin user "{admin_username}" already exists'))
            # Show password reminder for existing admin
            if not os.environ.get('ADMIN_PASSWORD'):
                self.stdout.write(self.style.SUCCESS(
                    f'📌 Default admin credentials:\n'
                    f'   Username: {admin_username}\n'
                    f'   Password: EduHelm@Admin2025\n'
                    f'   ⚠️  Change this password after first login!'
                ))
            return

        try:
            # Create admin user
            admin = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )

            # Create profile for admin
            profile, created = Profile.objects.get_or_create(
                user=admin,
                defaults={
                    'bio': 'System Administrator',
                    'is_mentor': True
                }
            )

            # Always show the password clearly in logs
            password_display = admin_password if not os.environ.get('ADMIN_PASSWORD') else "Set from ADMIN_PASSWORD env var"
            self.stdout.write(self.style.SUCCESS(
                f'\n{"="*60}\n'
                f'✅ ADMIN USER CREATED SUCCESSFULLY!\n'
                f'{"="*60}\n'
                f'📌 Save these credentials:\n'
                f'   Username: {admin_username}\n'
                f'   Email: {admin_email}\n'
                f'   Password: {password_display}\n'
                f'{"="*60}\n'
                f'⚠️  IMPORTANT: Change this password after first login!\n'
                f'{"="*60}\n'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating admin user: {str(e)}'))

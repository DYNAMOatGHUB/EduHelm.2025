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
        admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin@2025')

        # Check if admin exists
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(self.style.WARNING(f'Admin user "{admin_username}" already exists'))
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

            self.stdout.write(self.style.SUCCESS(
                f'✅ Admin user "{admin_username}" created successfully!\n'
                f'   Email: {admin_email}\n'
                f'   Password: {"Set from ADMIN_PASSWORD env var" if os.environ.get("ADMIN_PASSWORD") else admin_password}'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating admin user: {str(e)}'))

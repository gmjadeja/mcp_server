"""
Script to create a superuser if one doesn't exist
Run with: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_site.settings')
django.setup()

from django.contrib.auth.models import User

# Check if superuser exists
if User.objects.filter(is_superuser=True).exists():
    print("✅ Superuser already exists!")
    superuser = User.objects.filter(is_superuser=True).first()
    print(f"   Username: {superuser.username}")
    print(f"   Email: {superuser.email}")
else:
    print("Creating superuser...")
    username = "admin"
    email = "admin@mcp-server.ca"
    password = "admin123"  # Change this immediately after first login!
    
    # Create superuser
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print("✅ Superuser created successfully!")
    print(f"\nLogin credentials:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"\n⚠️  IMPORTANT: Change the password after first login!")
    print(f"   Visit: http://127.0.0.1:8000/admin/")


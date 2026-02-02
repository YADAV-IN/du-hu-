#!/usr/bin/env python
"""
DU HUB Website Quick Fix Script
Automatically fixes and initializes the website
"""

import os
import sys
import subprocess
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')

# Add project to path
sys.path.insert(0, '/workspaces/codespaces-django')

def run_command(cmd, description=""):
    """Run shell command"""
    if description:
        print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description or 'Command'} completed successfully")
            return True
        else:
            print(f"✗ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 DU HUB Website - Quick Fix Script")
    print("=" * 60)
    print()

    os.chdir('/workspaces/codespaces-django')

    # Step 1: Install dependencies
    print("📦 Step 1: Installing dependencies...")
    run_command('pip install -r requirements.txt -q', "Installing packages")
    print()

    # Step 2: Apply migrations
    print("🗄️  Step 2: Applying migrations...")
    run_command('python manage.py migrate', "Applying migrations")
    print()

    # Step 3: Initialize Django
    django.setup()
    
    # Step 4: Create admin user
    print("👤 Step 3: Creating admin user...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@duhub.local', 'admin123')
        print("✓ Admin user created: admin / admin123")
    else:
        print("✓ Admin user already exists")
    print()

    # Step 5: Create sample data
    print("📝 Step 4: Creating sample data...")
    from hello_world.core.models import Society, Event, Announcement, GlobalChatMessage
    from django.utils import timezone
    from datetime import timedelta

    if Society.objects.count() == 0:
        # Create societies
        societies_data = [
            {
                'name': 'Tech Society',
                'description': 'Dedicated to technology, innovation, and programming.',
                'color_theme': '#00ff00',
            },
            {
                'name': 'Cultural Club',
                'description': 'Celebrating arts, music, and cultural events.',
                'color_theme': '#ff00ff',
            },
            {
                'name': 'Sports Club',
                'description': 'Promoting sports and fitness activities.',
                'color_theme': '#00ffff',
            },
        ]

        for data in societies_data:
            society = Society.objects.create(**data, is_active=True, is_featured=True)
            print(f"✓ Created: {society.name}")

            # Create events for each society
            event = Event.objects.create(
                society=society,
                title=f"{society.name} Event 2026",
                description=f"Join our exciting {society.name} event!",
                event_type='workshop' if 'Tech' in society.name else 'cultural',
                event_date=timezone.now() + timedelta(days=7),
                location='Delhi University',
                is_featured=True
            )
            print(f"  ✓ Created event: {event.title}")

            # Create announcements
            announcement = Announcement.objects.create(
                society=society,
                title=f"{society.name} Announcement",
                content=f"Important news from {society.name}!",
                priority='high',
                is_active=True
            )
            print(f"  ✓ Created announcement: {announcement.title}")

        print()
        print("✓ Sample data created successfully")
    else:
        print("✓ Sample data already exists")
    print()

    # Summary
    print("=" * 60)
    print("✅ All fixes applied successfully!")
    print("=" * 60)
    print()
    print("📍 Access your website:")
    print("   🌐 Website:    http://localhost:8000")
    print("   🎛️  Admin:      http://localhost:8000/admin")
    print("   👤 Username:   admin")
    print("   🔐 Password:   admin123")
    print()
    print("🚀 Next step: python manage.py runserver 0.0.0.0:8000")
    print()

if __name__ == '__main__':
    main()

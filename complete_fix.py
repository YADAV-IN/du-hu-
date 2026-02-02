#!/usr/bin/env python
"""
Complete database fix script - Handles migration and data setup
Run with: python complete_fix.py
"""
import os
import sys
import shutil
import django
from pathlib import Path

# Add project to path
sys.path.insert(0, '/workspaces/codespaces-django')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from hello_world.core.models import Society, Event, Announcement

def main():
    print("\n" + "="*50)
    print("🔧 DU HUB Website Complete Fix")
    print("="*50 + "\n")
    
    db_path = Path('/workspaces/codespaces-django/db.sqlite3')
    
    # Step 1: Backup old database
    print("📦 Step 1: Backing up old database...")
    if db_path.exists():
        backup_path = Path('/workspaces/codespaces-django/db.sqlite3.backup')
        shutil.copy2(db_path, backup_path)
        db_path.unlink()
        print("✅ Backed up to db.sqlite3.backup\n")
    else:
        print("ℹ️  No existing database to backup\n")
    
    # Step 2: Apply all migrations
    print("🔄 Step 2: Applying all migrations...")
    try:
        call_command('migrate', verbosity=0, interactive=False)
        print("✅ Migrations applied successfully!\n")
    except Exception as e:
        print(f"❌ Migration failed: {e}\n")
        return False
    
    # Step 3: Create admin user
    print("👤 Step 3: Creating admin user...")
    try:
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@duhub.local', 'admin123')
            print("✅ Admin user created: admin / admin123\n")
        else:
            print("ℹ️  Admin user already exists\n")
    except Exception as e:
        print(f"❌ Failed to create admin: {e}\n")
    
    # Step 4: Create sample data
    print("📝 Step 4: Creating sample data...")
    try:
        if Society.objects.count() == 0:
            society = Society.objects.create(
                name="Coding Club",
                description="A club for all coding enthusiasts",
                banner_image="https://via.placeholder.com/1200x400?text=Coding+Club",
                logo_image="https://via.placeholder.com/200x200?text=CC",
                color_theme="#00d77a"
            )
            print(f"  ✅ Created society: {society.name}")
            
            # Create sample event
            event = Event.objects.create(
                society=society,
                title="Python Workshop",
                description="Learn Python programming",
                event_type="workshop",
                event_date=timezone.now() + timedelta(days=7),
                location="DU Campus",
                event_image="https://via.placeholder.com/400x300?text=Python+Workshop"
            )
            print(f"  ✅ Created event: {event.title}")
            
            # Create sample announcement
            announcement = Announcement.objects.create(
                society=society,
                title="New Member Registration",
                content="Registration for new members is now open!",
                priority="high"
            )
            print(f"  ✅ Created announcement: {announcement.title}\n")
        else:
            print("ℹ️  Sample data already exists\n")
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}\n")
        return False
    
    # Step 5: Display status
    print("✨ Database Status:")
    print(f"  📊 Societies: {Society.objects.count()}")
    print(f"  📅 Events: {Event.objects.count()}")
    print(f"  📢 Announcements: {Announcement.objects.count()}")
    
    print("\n" + "="*50)
    print("✨ Website Setup Complete!")
    print("="*50)
    print("\n🚀 Next steps:")
    print("  1. Start server: python manage.py runserver 0.0.0.0:8000")
    print("  2. Visit: http://localhost:8000")
    print("  3. Admin: http://localhost:8000/admin")
    print("  4. Login: admin / admin123\n")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

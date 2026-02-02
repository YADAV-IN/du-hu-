#!/bin/bash
# Complete website fix script - Resets and rebuilds database with all migrations

set -e

echo "=========================================="
echo "🔧 DU HUB Website Complete Fix"
echo "=========================================="

cd /workspaces/codespaces-django

echo ""
echo "📦 Step 1: Backing up old database..."
if [ -f db.sqlite3 ]; then
    mv db.sqlite3 db.sqlite3.backup
    echo "✅ Backed up to db.sqlite3.backup"
else
    echo "ℹ️  No existing database to backup"
fi

echo ""
echo "🗑️  Step 2: Removing migration state..."
find . -path "*/migrations/__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "🔄 Step 3: Creating fresh database with all migrations..."
python manage.py migrate --noinput

echo ""
echo "👤 Step 4: Creating admin user..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@duhub.local', 'admin123')
    print("✅ Admin user created: admin / admin123")
else:
    print("ℹ️  Admin user already exists")
END

echo ""
echo "📝 Step 5: Creating sample data..."
python manage.py shell << END
from hello_world.core.models import Society, Event, Announcement
from django.utils import timezone
from datetime import timedelta

# Create a sample society
if Society.objects.count() == 0:
    society = Society.objects.create(
        name="Coding Club",
        description="A club for all coding enthusiasts",
        banner_image="https://via.placeholder.com/1200x400?text=Coding+Club",
        logo_image="https://via.placeholder.com/200x200?text=CC",
        color_theme="#00d77a"
    )
    print(f"✅ Created sample society: {society.name}")
    
    # Create a sample event
    event = Event.objects.create(
        society=society,
        title="Python Workshop",
        description="Learn Python programming",
        event_type="workshop",
        event_date=timezone.now() + timedelta(days=7),
        location="DU Campus",
        event_image="https://via.placeholder.com/400x300?text=Python+Workshop"
    )
    print(f"✅ Created sample event: {event.title}")
    
    # Create a sample announcement
    announcement = Announcement.objects.create(
        society=society,
        title="New Member Registration",
        content="Registration for new members is now open!",
        priority="high"
    )
    print(f"✅ Created sample announcement: {announcement.title}")
else:
    print("ℹ️  Sample data already exists")
END

echo ""
echo "=========================================="
echo "✨ Website Setup Complete!"
echo "=========================================="
echo ""
echo "📊 Database Status:"
python manage.py shell << END
from hello_world.core.models import Society, Event, Announcement, GlobalChatMessage
print(f"  Societies: {Society.objects.count()}")
print(f"  Events: {Event.objects.count()}")
print(f"  Announcements: {Announcement.objects.count()}")
print(f"  Global Messages: {GlobalChatMessage.objects.count()}")
END

echo ""
echo "🚀 Next steps:"
echo "  1. Start the server: python manage.py runserver 0.0.0.0:8000"
echo "  2. Visit: http://localhost:8000"
echo "  3. Admin: http://localhost:8000/admin"
echo "  4. Login with: admin / admin123"
echo ""

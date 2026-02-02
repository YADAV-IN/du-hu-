#!/bin/bash

# DU HUB Website Fix Script
echo "🔧 DU HUB Website Repair & Fix"
echo "=============================="
echo ""

cd /workspaces/codespaces-django

# Step 1: Check Python
echo "1️⃣  Checking Python installation..."
python --version || python3 --version
echo "✓ Python found"
echo ""

# Step 2: Install dependencies
echo "2️⃣  Installing/Updating dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Step 3: Apply migrations
echo "3️⃣  Applying database migrations..."
python manage.py migrate
echo "✓ Migrations applied"
echo ""

# Step 4: Create sample admin user
echo "4️⃣  Setting up admin user..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@duhub.local', 'admin123')
    print("✓ Admin user created: username=admin, password=admin123")
else:
    print("✓ Admin user already exists")
END
echo ""

# Step 5: Create sample data
echo "5️⃣  Creating sample data..."
python manage.py shell << END
from hello_world.core.models import Society, Event, Announcement
from django.utils import timezone
from datetime import timedelta

# Create sample society if not exists
if Society.objects.count() == 0:
    society = Society.objects.create(
        name="Tech Society",
        description="A society dedicated to technology and innovation",
        color_theme="#00ff00",
        is_active=True,
        is_featured=True
    )
    print(f"✓ Created sample society: {society.name}")
    
    # Create sample event
    event = Event.objects.create(
        society=society,
        title="Tech Hackathon 2026",
        description="Join us for an exciting hackathon",
        event_type="competition",
        event_date=timezone.now() + timedelta(days=7),
        location="Delhi University",
        event_image="https://via.placeholder.com/400x300?text=Tech+Hackathon",
        is_featured=True
    )
    print(f"✓ Created sample event: {event.title}")
    
    # Create sample announcement
    announcement = Announcement.objects.create(
        society=society,
        title="New Event Announcement",
        content="We are excited to announce our upcoming tech hackathon!",
        priority="high",
        is_active=True
    )
    print(f"✓ Created sample announcement: {announcement.title}")
else:
    print("✓ Sample data already exists")
END
echo ""

echo "✅ All fixes applied successfully!"
echo ""
echo "Next steps:"
echo "1. Start the server: python manage.py runserver 0.0.0.0:8000"
echo "2. Visit website: http://localhost:8000"
echo "3. Access admin: http://localhost:8000/admin"
echo "4. Login with: username=admin, password=admin123"
echo ""

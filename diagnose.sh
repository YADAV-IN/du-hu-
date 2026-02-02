#!/bin/bash

# DU HUB Diagnostic Script
echo "🔍 DU HUB Diagnostic Report"
echo "==========================="
echo ""

cd /workspaces/codespaces-django

echo "📋 System Information"
echo "--------------------"
echo "Python Version:"
python --version 2>/dev/null || python3 --version
echo ""

echo "📦 Installed Packages"
echo "--------------------"
pip list | grep -i "django\|sqlite"
echo ""

echo "📂 Project Structure"
echo "-------------------"
echo "✓ Django Project: $([ -f 'manage.py' ] && echo 'Found' || echo 'NOT FOUND')"
echo "✓ App Directory: $([ -d 'hello_world/core' ] && echo 'Found' || echo 'NOT FOUND')"
echo "✓ Templates: $([ -d 'hello_world/templates' ] && echo 'Found' || echo 'NOT FOUND')"
echo "✓ Static Files: $([ -d 'hello_world/static' ] && echo 'Found' || echo 'NOT FOUND')"
echo "✓ Database: $([ -f 'db.sqlite3' ] && echo 'Found' || echo 'NOT FOUND')"
echo ""

echo "📝 Key Files Status"
echo "------------------"
echo "✓ models.py: $([ -f 'hello_world/core/models.py' ] && echo 'OK' || echo 'MISSING')"
echo "✓ views.py: $([ -f 'hello_world/core/views.py' ] && echo 'OK' || echo 'MISSING')"
echo "✓ admin.py: $([ -f 'hello_world/core/admin.py' ] && echo 'OK' || echo 'MISSING')"
echo "✓ urls.py: $([ -f 'hello_world/urls.py' ] && echo 'OK' || echo 'MISSING')"
echo "✓ base.html: $([ -f 'hello_world/templates/base.html' ] && echo 'OK' || echo 'MISSING')"
echo "✓ index.html: $([ -f 'hello_world/templates/index.html' ] && echo 'OK' || echo 'MISSING')"
echo "✓ android_modern.css: $([ -f 'hello_world/static/android_modern.css' ] && echo 'OK' || echo 'MISSING')"
echo ""

echo "🗄️  Database Information"
echo "----------------------"
python manage.py shell << END
from django.contrib.auth.models import User
from hello_world.core.models import Society, Event, Announcement, GlobalChatMessage
print(f"Users: {User.objects.count()}")
print(f"Societies: {Society.objects.count()}")
print(f"Events: {Event.objects.count()}")
print(f"Announcements: {Announcement.objects.count()}")
print(f"Global Chat Messages: {GlobalChatMessage.objects.count()}")
END
echo ""

echo "✅ Diagnostic complete!"
echo ""
echo "If you see any issues, run: bash fix_website.sh"
echo ""

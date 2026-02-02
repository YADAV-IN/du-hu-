#!/bin/bash

echo "🚀 DU HUB Startup Script"
echo "======================="

cd /workspaces/codespaces-django

echo "✓ Applying migrations..."
python manage.py migrate

echo "✓ Creating superuser (if needed)..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@duhub.local', 'admin')
    print("✓ Superuser created: admin / admin")
else:
    print("✓ Superuser already exists")
END

echo ""
echo "✓ Starting Django server..."
echo ""
echo "📍 Website:    http://localhost:8000"
echo "🎛️  Admin:      http://localhost:8000/admin"
echo "📚 Username:   admin"
echo "🔐 Password:   admin"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python manage.py runserver 0.0.0.0:8000

#!/bin/bash
# DU HUB - Important Commands Reference
# Quick copy-paste commands for common tasks

echo "════════════════════════════════════════════════════"
echo "  DU HUB - Important Commands Cheat Sheet"
echo "  By Ramlal Anand Student"
echo "════════════════════════════════════════════════════"
echo ""

# SETUP COMMANDS
cat << 'EOF'

📦 INITIAL SETUP
═══════════════════════════════════════════════════════

# 1. Install Dependencies
pip install -r requirements.txt

# 2. Create Database Tables
python manage.py makemigrations core
python manage.py migrate

# 3. Create Admin Account
python manage.py createsuperuser
# Username: admin
# Email: admin@duhub.com
# Password: (choose strong password)

# 4. Run Server
python manage.py runserver

# 5. Access Website
# Main Site: http://127.0.0.1:8000
# Admin Panel: http://127.0.0.1:8000/admin


🗃️ DATABASE COMMANDS
═══════════════════════════════════════════════════════

# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations status
python manage.py showmigrations

# Create migration for specific app
python manage.py makemigrations core

# Reset database (CAREFUL - deletes all data!)
# Windows:
del db.sqlite3
python manage.py migrate

# Mac/Linux:
rm db.sqlite3
python manage.py migrate


📊 ADMIN & USER COMMANDS
═══════════════════════════════════════════════════════

# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username

# Access Django shell
python manage.py shell

# Load sample data
python manage.py shell < create_sample_data.py


🎨 STATIC FILES COMMANDS
═══════════════════════════════════════════════════════

# Collect static files
python manage.py collectstatic

# Clear collected static files
python manage.py collectstatic --clear

# Don't ask for confirmation
python manage.py collectstatic --noinput


🔍 DEBUGGING COMMANDS
═══════════════════════════════════════════════════════

# Check for errors
python manage.py check

# Validate models
python manage.py validate

# Show SQL for migration
python manage.py sqlmigrate core 0001

# Start shell with Django
python manage.py shell


🌐 SERVER COMMANDS
═══════════════════════════════════════════════════════

# Run development server (default port 8000)
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Run on specific address
python manage.py runserver 0.0.0.0:8000

# Access from network
python manage.py runserver 0.0.0.0:8000
# Then access: http://YOUR-IP:8000


🔧 GIT COMMANDS
═══════════════════════════════════════════════════════

# Initialize Git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: DU HUB by Ramlal Anand Student"

# Connect to GitHub
git remote add origin https://github.com/YOUR-USERNAME/du-hub.git

# Push to GitHub
git branch -M main
git push -u origin main

# Check status
git status

# View commit history
git log --oneline

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature-name

# Switch branch
git checkout main

# Merge branch
git merge feature-name


📝 DJANGO SHELL COMMANDS
═══════════════════════════════════════════════════════

# Start Django shell
python manage.py shell

# Inside shell - Import models
from hello_world.core.models import Society, Event, Announcement

# Create a society
society = Society.objects.create(
    name="Tech Society",
    description="Technology club",
    color_theme="#00ff00"
)

# Query all societies
societies = Society.objects.all()

# Filter societies
active = Society.objects.filter(is_active=True)

# Get specific society
society = Society.objects.get(id=1)

# Update society
society.name = "New Name"
society.save()

# Delete society
society.delete()

# Exit shell
exit()


🧪 TESTING COMMANDS
═══════════════════════════════════════════════════════

# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test core

# Run with verbose output
python manage.py test --verbosity=2


🗑️ CLEANUP COMMANDS
═══════════════════════════════════════════════════════

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Windows:
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# Remove migration files (keep __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Clear old sessions
python manage.py clearsessions


💾 BACKUP COMMANDS
═══════════════════════════════════════════════════════

# Backup database
cp db.sqlite3 db_backup.sqlite3

# Windows:
copy db.sqlite3 db_backup.sqlite3

# Export data to JSON
python manage.py dumpdata > backup.json

# Export specific app
python manage.py dumpdata core > core_backup.json

# Import data from JSON
python manage.py loaddata backup.json


🔄 UPDATE & MAINTENANCE
═══════════════════════════════════════════════════════

# Update requirements file
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Upgrade Django
pip install --upgrade django

# Check Django version
python -m django --version


🐛 TROUBLESHOOTING
═══════════════════════════════════════════════════════

# Port already in use
python manage.py runserver 8080

# Permission denied
sudo python manage.py runserver  # Linux/Mac

# Module not found
pip install -r requirements.txt

# Database locked
rm db.sqlite3-journal
python manage.py migrate

# Static files not loading
python manage.py collectstatic --clear
python manage.py collectstatic

# CSRF errors
# Check CSRF_TRUSTED_ORIGINS in settings.py

# Migration conflicts
python manage.py migrate --fake
python manage.py makemigrations
python manage.py migrate


📱 PRODUCTION COMMANDS
═══════════════════════════════════════════════════════

# Before deployment checklist:
# 1. Set DEBUG = False
# 2. Update ALLOWED_HOSTS
# 3. Change SECRET_KEY
# 4. Use PostgreSQL/MySQL
# 5. Setup HTTPS
# 6. Configure static files
# 7. Setup environment variables

# Collect static for production
python manage.py collectstatic --noinput

# Use production server (Gunicorn)
pip install gunicorn
gunicorn hello_world.wsgi:application


🔐 SECURITY COMMANDS
═══════════════════════════════════════════════════════

# Generate new SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Check security issues
python manage.py check --deploy


📊 DATABASE QUERIES (Django Shell)
═══════════════════════════════════════════════════════

python manage.py shell

# Count objects
Society.objects.count()
Event.objects.count()

# Get latest
Event.objects.latest('created_at')

# Order by
Event.objects.order_by('-event_date')

# Filter and count
Event.objects.filter(is_featured=True).count()

# Complex queries
from django.utils import timezone
Event.objects.filter(event_date__gte=timezone.now())


🎯 QUICK START SEQUENCE
═══════════════════════════════════════════════════════

# Complete setup in one go:
pip install -r requirements.txt && \
python manage.py makemigrations core && \
python manage.py migrate && \
echo "Now create superuser:" && \
python manage.py createsuperuser


📋 DAILY DEVELOPMENT WORKFLOW
═══════════════════════════════════════════════════════

# 1. Pull latest code
git pull origin main

# 2. Apply any new migrations
python manage.py migrate

# 3. Run server
python manage.py runserver

# 4. Make changes...

# 5. Add and commit
git add .
git commit -m "Description of changes"

# 6. Push to GitHub
git push origin main


EOF

echo ""
echo "════════════════════════════════════════════════════"
echo "  📖 For more help, see documentation files:"
echo "     - QUICK_START_GUIDE.md"
echo "     - DU_HUB_README.md"
echo "     - GITHUB_DEPLOYMENT_GUIDE.md"
echo "════════════════════════════════════════════════════"

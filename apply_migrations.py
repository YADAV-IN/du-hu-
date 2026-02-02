#!/usr/bin/env python
"""
Quick script to apply all pending migrations and recreate the database
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from django.core.management import call_command

print("🚀 Applying all pending migrations...")
try:
    call_command('migrate', verbosity=2)
    print("✅ Migrations applied successfully!")
except Exception as e:
    print(f"❌ Migration failed: {e}")
    sys.exit(1)

print("\n📊 Database migration complete!")
print("Database is now ready to use!")

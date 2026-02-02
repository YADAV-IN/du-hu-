#!/usr/bin/env python3
import os, sys, django
os.chdir('/workspaces/codespaces-django')
sys.path.insert(0, '/workspaces/codespaces-django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hello_world.settings'
django.setup()
from django.core.management import call_command
from django.contrib.auth.models import User

print("🔄 Applying all migrations...")
call_command('migrate', '--noinput')
print("✅ Migrations done!")

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@du.local', 'admin123')
    print("✅ Admin created: admin/admin123")
else:
    print("ℹ️  Admin exists")

from hello_world.core.models import Society, Event, Announcement, SocietyMember, SocietyGallery, SocietyAchievement
from django.utils import timezone
from datetime import timedelta, date

if Society.objects.count() == 0:
    # Create Tech Society
    s1 = Society.objects.create(
        name="Tech Society DU",
        tagline="Innovate. Build. Transform.",
        description="The official technology society of Delhi University fostering innovation and technical excellence.",
        long_description="Tech Society DU is the premier technology club at Delhi University...",
        category="technical",
        color_theme="#00d77a",
        is_featured=True,
        is_verified=True,
        member_count=150,
        founding_year=2018,
        president_name="Rahul Sharma",
        vice_president="Priya Singh",
        convenor_name="Neha Verma",
        faculty_advisor="Dr. A.K. Gupta",
        email="tech@du.ac.in",
        instagram="https://instagram.com/techsocietydu",
        linkedin="https://linkedin.com/company/techsocietydu"
    )
    
    # Create Cultural Society
    s2 = Society.objects.create(
        name="Rang Cultural Society",
        tagline="Colors of Expression",
        description="Celebrating art, music, dance and cultural heritage of India.",
        category="cultural",
        color_theme="#ff4081",
        is_featured=True,
        member_count=200,
        founding_year=2015,
        president_name="Ananya Kapoor",
        convenor_name="Sahil Mehta"
    )
    
    # Create Events
    Event.objects.create(
        society=s1,
        title="Hackathon 2026",
        description="24-hour coding marathon with amazing prizes",
        event_type="competition",
        event_date=timezone.now() + timedelta(days=10),
        location="Main Campus Auditorium",
        event_image="https://via.placeholder.com/400x300?text=Hackathon+2026"
    )
    
    Event.objects.create(
        society=s2,
        title="Cultural Fest - Rang Utsav",
        description="Annual cultural extravaganza",
        event_type="cultural",
        event_date=timezone.now() + timedelta(days=20),
        location="Open Air Theatre"
    )
    
    # Create Announcements
    Announcement.objects.create(
        society=s1,
        title="New Member Registration Open!",
        content="Join our tech family today!",
        priority="high"
    )
    
    # Create Members
    SocietyMember.objects.create(society=s1, name="Rahul Sharma", role="president", order=1)
    SocietyMember.objects.create(society=s1, name="Priya Singh", role="vice_president", order=2)
    SocietyMember.objects.create(society=s1, name="Neha Verma", role="convenor", order=3)
    SocietyMember.objects.create(society=s1, name="Amit Kumar", role="tech_head", order=4)
    
    # Create Achievements
    SocietyAchievement.objects.create(
        society=s1,
        title="Best Tech Society Award",
        description="Won the best tech society award at National Level",
        achievement_date=date(2025, 12, 15),
        icon="🏆"
    )
    
    # Create Gallery
    SocietyGallery.objects.create(
        society=s1,
        title="Hackathon 2025 Winners",
        image_url="https://via.placeholder.com/600x400?text=Hackathon+Winners",
        is_featured=True,
        likes_count=42
    )
    
    print("✅ Sample data with advanced features created!")
else:
    print("ℹ️  Data already exists")

print("\n✨ Setup complete!")
print("🚀 Run: python manage.py runserver 0.0.0.0:8000")
print("🌐 Visit: http://localhost:8000")
print("👤 Admin: http://localhost:8000/admin (admin/admin123)")

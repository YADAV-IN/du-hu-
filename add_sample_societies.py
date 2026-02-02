#!/usr/bin/env python
"""
Script to add sample societies to the database
"""
import os
import django
import secrets

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_world.settings')
django.setup()

from hello_world.core.models import Society, Event
from django.utils import timezone
from datetime import timedelta

# Sample societies data
societies_data = [
    {
        'name': 'Tech Society',
        'tagline': 'Innovation & Code',
        'description': 'Technology club for coding and innovation',
        'color_theme': '#00d77a',
        'category': 'technical',
        'is_verified': True,
        'member_count': 150,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
    {
        'name': 'Drama Club',
        'tagline': 'Express Yourself',
        'description': 'Join us for theater, acting, and performance arts',
        'color_theme': '#FF6B9D',
        'category': 'cultural',
        'is_verified': True,
        'member_count': 120,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
    {
        'name': 'Photography Society',
        'tagline': 'Capture Moments',
        'description': 'Learn and share photography with fellow enthusiasts',
        'color_theme': '#4ECDC4',
        'category': 'music',
        'is_verified': True,
        'member_count': 95,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
    {
        'name': 'Debate Club',
        'tagline': 'Speak & Persuade',
        'description': 'Develop critical thinking through debates and discussions',
        'color_theme': '#A29BFE',
        'category': 'debate',
        'is_verified': True,
        'member_count': 110,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
    {
        'name': 'Music Band',
        'tagline': 'Make Some Noise',
        'description': 'Play, compose, and celebrate music together',
        'color_theme': '#FFA502',
        'category': 'music',
        'is_verified': True,
        'member_count': 85,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
    {
        'name': 'Sports Committee',
        'tagline': 'Stay Active',
        'description': 'Organize and participate in various sports events',
        'color_theme': '#FF3838',
        'category': 'sports',
        'is_verified': True,
        'member_count': 200,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
    {
        'name': 'Literary Society',
        'tagline': 'Words Matter',
        'description': 'Celebrate literature, poetry, and creative writing',
        'color_theme': '#6C63FF',
        'category': 'literary',
        'is_verified': True,
        'member_count': 75,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
    {
        'name': 'Entrepreneurship Club',
        'tagline': 'Build Your Dream',
        'description': 'Mentorship and networking for aspiring entrepreneurs',
        'color_theme': '#00D4FF',
        'category': 'technical',
        'is_verified': True,
        'member_count': 130,
        'access_code': secrets.token_urlsafe(12)[:20],
    },
]

# Clear existing societies
Society.objects.all().delete()
print("Cleared existing societies")

# Add new societies
for data in societies_data:
    society = Society.objects.create(**data)
    print(f"Created: {society.name} - Code: {society.access_code}")

    # Add sample event for this society
    Event.objects.create(
        society=society,
        title=f"{society.name} - Welcome Event",
        description=f"Join us for an exciting event with {society.name}",
        event_date=timezone.now() + timedelta(days=7),
        location="Delhi University",
        event_type='workshop',
    )
    print(f"  Added event for {society.name}")

print(f"\n✓ Total societies created: {Society.objects.count()}")

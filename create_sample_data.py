# DU HUB - Sample Data Creation Script
# Run this in Django shell: python manage.py shell < create_sample_data.py

from hello_world.core.models import Society, Event, Announcement, GlobalChatMessage
from django.utils import timezone
from datetime import timedelta

print("Creating sample data for DU HUB...")

# Create Societies
societies_data = [
    {
        'name': 'Tech Society',
        'description': 'Exploring technology, coding, and innovation. Join us for workshops, hackathons, and tech talks!',
        'color_theme': '#00ff00',
        'is_active': True
    },
    {
        'name': 'Cultural Society',
        'description': 'Celebrating art, music, dance, and cultural heritage. Experience the diversity of our campus!',
        'color_theme': '#33ff33',
        'is_active': True
    },
    {
        'name': 'Sports Society',
        'description': 'Promoting fitness, sportsmanship, and athletic excellence. Get active and stay healthy!',
        'color_theme': '#00cc00',
        'is_active': True
    },
    {
        'name': 'Literary Society',
        'description': 'For book lovers, writers, and poetry enthusiasts. Share your stories and ideas!',
        'color_theme': '#39ff14',
        'is_active': True
    },
]

societies = []
for data in societies_data:
    society, created = Society.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    societies.append(society)
    if created:
        print(f"✅ Created society: {society.name}")
    else:
        print(f"ℹ️  Society already exists: {society.name}")

# Create Events
events_data = [
    {
        'society': societies[0],  # Tech Society
        'title': 'Web Development Workshop',
        'description': 'Learn modern web development with Django and React. Hands-on workshop for beginners!',
        'event_type': 'workshop',
        'event_date': timezone.now() + timedelta(days=5),
        'location': 'Computer Lab, Block A',
        'is_featured': True
    },
    {
        'society': societies[0],  # Tech Society
        'title': 'Hackathon 2026',
        'description': '24-hour coding challenge. Build innovative solutions and win prizes!',
        'event_type': 'competition',
        'event_date': timezone.now() + timedelta(days=15),
        'location': 'Main Auditorium',
        'is_featured': True
    },
    {
        'society': societies[1],  # Cultural Society
        'title': 'Annual Cultural Fest',
        'description': 'Three days of music, dance, drama, and fun. Join us for the biggest event of the year!',
        'event_type': 'cultural',
        'event_date': timezone.now() + timedelta(days=30),
        'location': 'College Ground',
        'is_featured': True
    },
    {
        'society': societies[2],  # Sports Society
        'title': 'Inter-College Basketball Tournament',
        'description': 'Compete with the best teams. Show your skills on the court!',
        'event_type': 'sports',
        'event_date': timezone.now() + timedelta(days=10),
        'location': 'Sports Complex',
        'is_featured': False
    },
    {
        'society': societies[3],  # Literary Society
        'title': 'Poetry Slam Night',
        'description': 'Share your original poetry. Open mic for all aspiring poets!',
        'event_type': 'other',
        'event_date': timezone.now() + timedelta(days=7),
        'location': 'Seminar Hall',
        'is_featured': False
    },
]

for data in events_data:
    event, created = Event.objects.get_or_create(
        title=data['title'],
        society=data['society'],
        defaults=data
    )
    if created:
        print(f"✅ Created event: {event.title}")

# Create Announcements
announcements_data = [
    {
        'society': societies[0],
        'title': 'Workshop Registration Open',
        'content': 'Register now for the upcoming Web Development Workshop. Limited seats available!',
        'priority': 'high',
        'is_active': True
    },
    {
        'society': societies[1],
        'title': 'Auditions for Cultural Fest',
        'content': 'Auditions for dance, music, and drama performances start next week. Prepare your acts!',
        'priority': 'medium',
        'is_active': True
    },
    {
        'society': societies[2],
        'title': 'Sports Kit Distribution',
        'content': 'Collect your sports kits from the sports room. Timing: 9 AM to 5 PM',
        'priority': 'low',
        'is_active': True
    },
    {
        'society': societies[3],
        'title': 'Submit Your Stories',
        'content': 'We are publishing a college magazine. Submit your short stories and poems by next Friday.',
        'priority': 'medium',
        'is_active': True
    },
]

for data in announcements_data:
    announcement, created = Announcement.objects.get_or_create(
        title=data['title'],
        society=data['society'],
        defaults=data
    )
    if created:
        print(f"✅ Created announcement: {announcement.title}")

# Create Sample Chat Messages
chat_messages = [
    {'user_name': 'Rahul', 'message': 'Hey everyone! Excited for the upcoming events!'},
    {'user_name': 'Priya', 'message': 'Who is attending the hackathon?'},
    {'user_name': 'Amit', 'message': 'The cultural fest is going to be amazing!'},
    {'user_name': 'Sneha', 'message': 'Looking forward to the poetry slam!'},
]

for data in chat_messages:
    msg, created = GlobalChatMessage.objects.get_or_create(
        user_name=data['user_name'],
        message=data['message']
    )
    if created:
        print(f"✅ Created chat message from: {msg.user_name}")

print("\n🎉 Sample data created successfully!")
print("👉 Access the admin panel to manage content: http://127.0.0.1:8000/admin/")
print("👉 Visit the website: http://127.0.0.1:8000/")

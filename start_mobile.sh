#!/bin/bash
# Mobile-First Android Optimization - Quick Start Script

echo "🚀 DU HUB Mobile Optimization Started..."
echo ""

# Apply migrations
echo "📦 Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create sample data
echo "📝 Creating sample data..."
python FIX.py

# Start server
echo "🌐 Starting development server..."
echo "✨ Open in Android browser: http://localhost:8000"
echo ""
python manage.py runserver 0.0.0.0:8000

#!/bin/bash
# DU HUB - Quick Setup Script
# This script sets up the DU HUB website automatically

echo "🌟 ========================================= 🌟"
echo "   DU HUB - Unofficial Student Portal Setup"
echo "   By Ramlal Anand Student"
echo "🌟 ========================================= 🌟"
echo ""

# Step 1: Apply migrations
echo "📦 Step 1: Creating database tables..."
python manage.py makemigrations core
python manage.py migrate

echo ""
echo "✅ Database setup complete!"
echo ""

# Step 2: Collect static files
echo "🎨 Step 2: Setting up static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Static files ready!"
echo ""

# Step 3: Create sample data
echo "📝 Step 3: Would you like to create a superuser (admin account)?"
echo "This will allow you to access the admin panel at /admin/"
read -p "Create superuser? (y/n): " CREATE_SUPERUSER

if [ "$CREATE_SUPERUSER" = "y" ] || [ "$CREATE_SUPERUSER" = "Y" ]; then
    echo ""
    echo "Creating superuser account..."
    python manage.py createsuperuser
fi

echo ""
echo "🎉 ========================================= 🎉"
echo "   Setup Complete!"
echo "🎉 ========================================= 🎉"
echo ""
echo "📋 Next Steps:"
echo "   1. Run the server: python manage.py runserver"
echo "   2. Open browser: http://127.0.0.1:8000/"
echo "   3. Access admin: http://127.0.0.1:8000/admin/"
echo "   4. Add societies, events, and announcements"
echo ""
echo "📖 For detailed instructions, see DU_HUB_README.md"
echo ""
echo "🌈 Happy coding! - Ramlal Anand Student"
echo ""

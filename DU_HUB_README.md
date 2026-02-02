# DU HUB - Unofficial Student Portal
### By Ramlal Anand Student

## 🌟 Overview
DU HUB is an advanced, modern student portal designed for college students. It features society management, event announcements, real-time chat, and a beautiful black & green themed UI.

## ✨ Features

### 🎯 Core Features
- **Multiple Societies**: Each society has its own dedicated page
- **Event Management**: Comprehensive event listings with categories
- **Announcements System**: Priority-based announcement ticker
- **Global Chat**: Real-time chat for all users
- **Society Chat**: Individual chat rooms for each society
- **Beautiful UI**: Modern black & green color scheme with animations
- **Responsive Design**: Works perfectly on all devices

### 🎨 Design Highlights
- Unique animated logo with pulse effect
- Smooth transitions and hover effects
- Gradient backgrounds and glowing text effects
- Modern card-based layout
- Scrolling announcement ticker
- Custom scrollbars
- Mobile-responsive navigation

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd codespaces-django
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations**
   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   ```

4. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the website**
   - Main Site: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 📱 Usage Guide

### Admin Panel
1. Login to admin panel at `/admin/`
2. Add Societies with:
   - Name
   - Description
   - Banner image URL (optional)
   - Custom color theme
3. Create Events for each society
4. Post Announcements with priority levels
5. Monitor chat messages

### Main Features

#### Societies
- Each society has a dedicated page
- Custom banners and posters
- Individual chat rooms
- Event listings
- Announcements feed

#### Events
- Multiple event types (Workshop, Seminar, Competition, etc.)
- Date and location information
- Registration links
- Featured events highlight

#### Chat System
- **Global Chat**: Available on homepage for all users
- **Society Chat**: Each society has its own chat room
- Real-time message updates (auto-refresh every 5 seconds)
- Simple username + message system

## 🎨 Color Scheme
- **Primary Green**: #00ff00
- **Dark Green**: #00cc00
- **Light Green**: #33ff33
- **Neon Green**: #39ff14
- **Black Background**: #000000
- **Dark Gray**: #0a0a0a, #1a1a1a, #2a2a2a

## 📂 Project Structure
```
codespaces-django/
├── hello_world/
│   ├── core/
│   │   ├── models.py          # Database models
│   │   ├── views.py           # View functions
│   │   ├── admin.py           # Admin configuration
│   │   └── __pycache__/
│   ├── static/
│   │   └── duhub.css          # Main stylesheet
│   ├── templates/
│   │   ├── base.html          # Base template
│   │   ├── index.html         # Homepage
│   │   ├── society_detail.html # Society page
│   │   └── all_events.html    # Events listing
│   ├── settings.py            # Django settings
│   └── urls.py                # URL routing
├── manage.py
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database
Default: SQLite (db.sqlite3)
Can be configured to use PostgreSQL or MySQL in settings.py

## 🌐 API Endpoints

### Chat APIs
- `POST /api/chat/global/` - Send global message
- `GET /api/chat/global/messages/` - Get global messages
- `POST /api/chat/society/<id>/` - Send society message
- `GET /api/chat/society/<id>/messages/` - Get society messages

### Pages
- `/` - Homepage
- `/events/` - All events
- `/society/<id>/` - Individual society page
- `/admin/` - Admin panel

## 🎯 Models

### Society
- name, description
- banner_image, poster_image
- color_theme
- is_active status

### Event
- title, description
- event_type, event_date, location
- registration_link, image
- is_featured flag
- Linked to Society

### Announcement
- title, content
- priority (low, medium, high, urgent)
- expires_at date
- is_active status
- Linked to Society

### Chat Messages
- GlobalChatMessage - for main chat
- SocietyChatMessage - for society chats
- user_name, message, created_at

## 🎨 Customization

### Changing Colors
Edit `/hello_world/static/duhub.css`:
```css
:root {
    --primary-green: #00ff00;  /* Change to your color */
    --black: #000000;          /* Change background */
}
```

### Adding New Societies
1. Go to Admin Panel
2. Add new Society
3. Set custom color theme for each society
4. Add events and announcements

## 📱 Mobile Responsive
- Adaptive navigation
- Responsive grids
- Touch-friendly chat interface
- Optimized for all screen sizes

## 🔒 Security Features
- CSRF protection enabled
- XSS protection in templates
- Secure admin panel
- Input validation

## 🐛 Troubleshooting

### Common Issues

**CSS not loading?**
```bash
python manage.py collectstatic
```

**Database errors?**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Port already in use?**
```bash
python manage.py runserver 8080
```

## 📝 Future Enhancements
- [ ] User authentication system
- [ ] File upload for banners/posters
- [ ] WebSocket for real-time chat
- [ ] Email notifications
- [ ] Social media integration
- [ ] Event calendar view
- [ ] Search functionality
- [ ] Dark/Light theme toggle

## 👨‍💻 Developer
**Ramlal Anand Student**

## 📄 License
This is an unofficial student project for educational purposes.

## 🤝 Contributing
This is a student project. Feel free to fork and enhance!

## 📞 Support
For issues or questions, please check the code or create an issue in the repository.

---

### Quick Start Commands
```bash
# Install
pip install -r requirements.txt

# Setup Database
python manage.py makemigrations core
python manage.py migrate

# Create Admin
python manage.py createsuperuser

# Run Server
python manage.py runserver

# Access Site
http://127.0.0.1:8000
```

---

**Built with ❤️ for DU Students**
**DU HUB - Connecting Students, Building Communities**

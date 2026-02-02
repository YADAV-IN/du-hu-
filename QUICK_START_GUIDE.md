# 🚀 DU HUB - Quick Start Guide

## ⚡ Super Fast Setup (5 Minutes)

### For Beginners - Simple Steps

#### 1️⃣ Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux**: Press `Ctrl + Alt + T` or search "Terminal"

#### 2️⃣ Navigate to Project Folder
```bash
cd path/to/codespaces-django
```

#### 3️⃣ Run Setup Commands
Copy and paste these commands one by one:

```bash
# Install required packages
pip install -r requirements.txt

# Setup database
python manage.py makemigrations core
python manage.py migrate

# Create admin account
python manage.py createsuperuser
```

When creating superuser:
- **Username**: admin (or your choice)
- **Email**: your@email.com (can be fake)
- **Password**: Choose a strong password

#### 4️⃣ Start the Server
```bash
python manage.py runserver
```

#### 5️⃣ Open Your Browser
Go to: **http://127.0.0.1:8000**

---

## 🎯 First Time Using the Website

### Access Admin Panel
1. Go to: **http://127.0.0.1:8000/admin**
2. Login with your superuser credentials
3. You'll see the admin dashboard

### Add Your First Society
1. Click on **"Societies"** → **"Add Society"**
2. Fill in:
   - **Name**: "Tech Club"
   - **Description**: "Technology and coding enthusiasts"
   - **Color theme**: `#00ff00` (or any hex color)
   - Check **"Is active"**
3. Click **"Save"**

### Add an Event
1. Click on **"Events"** → **"Add Event"**
2. Fill in:
   - **Society**: Select the society you created
   - **Title**: "Web Development Workshop"
   - **Description**: "Learn Django and web development"
   - **Event type**: Workshop
   - **Event date**: Choose a future date
   - **Location**: "Computer Lab"
3. Click **"Save"**

### Add an Announcement
1. Click on **"Announcements"** → **"Add Announcement"**
2. Fill in:
   - **Society**: Select your society
   - **Title**: "Registration Open"
   - **Content**: "Register for the workshop now!"
   - **Priority**: High
   - Check **"Is active"**
3. Click **"Save"**

### View Your Website
1. Go to: **http://127.0.0.1:8000**
2. You should see:
   - Your society in the societies section
   - Your event in upcoming events
   - Your announcement in the ticker
3. Try the **Global Chat** at the bottom!

---

## 🛠️ Common Commands

### Start Server
```bash
python manage.py runserver
```

### Stop Server
Press `Ctrl + C` in the terminal

### Create Admin Account (if you skipped it)
```bash
python manage.py createsuperuser
```

### Reset Database (Start Fresh)
```bash
# Delete the database file
# Windows:
del db.sqlite3
# Mac/Linux:
rm db.sqlite3

# Recreate database
python manage.py migrate
python manage.py createsuperuser
```

### Add Sample Data
```bash
python manage.py shell < create_sample_data.py
```

---

## 🎨 Customization Tips

### Change Color Theme
1. Open: `hello_world/static/duhub.css`
2. Find line with `:root {`
3. Change colors:
```css
--primary-green: #00ff00;  /* Your color here */
--black: #000000;          /* Background color */
```

### Change Website Name
1. Open: `hello_world/templates/base.html`
2. Find `<h1>DU HUB</h1>`
3. Change to your name

### Change Footer Text
1. Open: `hello_world/templates/base.html`
2. Find `<footer class="footer">`
3. Edit the text

---

## 🐛 Troubleshooting

### "No module named 'django'"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### "Port 8000 is already in use"
**Solution**: Use different port
```bash
python manage.py runserver 8080
```
Then visit: http://127.0.0.1:8080

### CSS not showing
**Solution**: Hard refresh browser
- **Windows/Linux**: `Ctrl + Shift + R`
- **Mac**: `Cmd + Shift + R`

### Can't login to admin
**Solution**: Create new superuser
```bash
python manage.py createsuperuser
```

### Database errors
**Solution**: Reset database
```bash
# Delete db.sqlite3 file
# Then run:
python manage.py migrate
```

---

## 📱 Testing the Website

### Things to Try:
1. ✅ Create multiple societies with different colors
2. ✅ Add events for each society
3. ✅ Post announcements with different priorities
4. ✅ Send messages in global chat
5. ✅ Click on a society to see its page
6. ✅ Try the society-specific chat
7. ✅ View all events page
8. ✅ Test on mobile (make browser window small)

---

## 🌐 Upload to GitHub (Simple)

### Step 1: Create GitHub Account
Go to: https://github.com and sign up

### Step 2: Install Git
- **Windows**: Download from https://git-scm.com
- **Mac**: Already installed or use `brew install git`
- **Linux**: `sudo apt install git`

### Step 3: Push to GitHub
```bash
# In project folder
git init
git add .
git commit -m "Initial commit: DU HUB website"

# Create new repository on GitHub
# Then connect and push:
git remote add origin https://github.com/YOUR-USERNAME/your-repo-name.git
git branch -M main
git push -u origin main
```

**Detailed guide**: See `GITHUB_DEPLOYMENT_GUIDE.md`

---

## 📋 Project Files Explained

| File/Folder | What It Does |
|-------------|--------------|
| `manage.py` | Django command tool |
| `db.sqlite3` | Your database (contains all data) |
| `requirements.txt` | List of required packages |
| `hello_world/` | Main project folder |
| `core/` | Website app with models, views |
| `templates/` | HTML files for pages |
| `static/` | CSS and images |
| `settings.py` | Website configuration |
| `urls.py` | URL routing |

---

## 🎯 What's Next?

### Beginner Tasks:
1. Add 5 different societies
2. Create 10 events
3. Post announcements
4. Customize colors
5. Change website title

### Intermediate Tasks:
1. Add images for society banners
2. Create more event types
3. Customize CSS styles
4. Add more pages

### Advanced Tasks:
1. Add user authentication
2. Implement file uploads
3. Create email notifications
4. Deploy to internet

---

## 📞 Need Help?

### Check These Files:
- `DU_HUB_README.md` - Full documentation
- `GITHUB_DEPLOYMENT_GUIDE.md` - Git & GitHub help
- `create_sample_data.py` - Example data

### Online Resources:
- Django Documentation: https://docs.djangoproject.com
- Python Tutorial: https://python.org
- CSS Guide: https://developer.mozilla.org

---

## ✅ Success Checklist

- [ ] Python installed
- [ ] Packages installed (`pip install -r requirements.txt`)
- [ ] Database created (`python manage.py migrate`)
- [ ] Superuser created
- [ ] Server running
- [ ] Website opens in browser
- [ ] Admin panel accessible
- [ ] At least one society added
- [ ] At least one event added
- [ ] Chat working

---

## 🎉 Congratulations!

Your DU HUB website is now running!

**Access Points:**
- 🌐 Main Website: http://127.0.0.1:8000
- 🔐 Admin Panel: http://127.0.0.1:8000/admin
- 📅 Events Page: http://127.0.0.1:8000/events/

**Made with ❤️ by Ramlal Anand Student**

---

**Pro Tip:** Bookmark the admin panel for easy access!

# 🚀 DU HUB - Git & GitHub Deployment Guide

## Step-by-Step Guide to Push Your Website to GitHub

### Prerequisites
- Git installed on your computer
- GitHub account created
- Terminal/Command Prompt access

---

## 📋 Method 1: Create New Repository on GitHub

### Step 1: Initialize Git Repository
```bash
cd /workspaces/codespaces-django
git init
```

### Step 2: Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Add All Files
```bash
git add .
```

### Step 4: Create First Commit
```bash
git commit -m "Initial commit: DU HUB - Unofficial Student Portal by Ramlal Anand Student"
```

### Step 5: Create Repository on GitHub
1. Go to https://github.com
2. Click on "+" icon → "New repository"
3. Name it: `du-hub-student-portal`
4. Description: `DU HUB - Unofficial Student Portal with societies, events, chat features`
5. Choose Public or Private
6. **DO NOT** initialize with README (we already have one)
7. Click "Create repository"

### Step 6: Connect Local to GitHub
```bash
# Replace YOUR-USERNAME with your GitHub username
git remote add origin https://github.com/YOUR-USERNAME/du-hub-student-portal.git
```

### Step 7: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

---

## 📋 Method 2: If Repository Already Exists

### Update Existing Repository
```bash
# Add all changes
git add .

# Commit changes
git commit -m "Updated DU HUB website with new features"

# Push to GitHub
git push origin main
```

---

## 🔐 Authentication Issues?

### Option 1: Use Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. When pushing, use token as password

### Option 2: Use SSH Key
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Then use SSH URL
git remote set-url origin git@github.com:YOUR-USERNAME/du-hub-student-portal.git
```

---

## 📂 What Gets Uploaded

### Files Included:
✅ All Python files (.py)
✅ HTML templates
✅ CSS files
✅ README files
✅ requirements.txt
✅ manage.py
✅ Setup scripts

### Files Excluded (Add to .gitignore):
❌ db.sqlite3 (database)
❌ __pycache__/ (Python cache)
❌ .env (environment variables)
❌ venv/ (virtual environment)

---

## 📝 Create .gitignore File

Create a file named `.gitignore` with this content:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/static

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

Then commit it:
```bash
git add .gitignore
git commit -m "Add .gitignore file"
git push
```

---

## 🌟 Useful Git Commands

### Check Status
```bash
git status
```

### View Commit History
```bash
git log --oneline
```

### Create a Branch
```bash
git checkout -b feature-name
```

### Merge Branch
```bash
git checkout main
git merge feature-name
```

### Pull Latest Changes
```bash
git pull origin main
```

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

---

## 📱 Making Your Repository Look Professional

### Add Repository Details
1. Go to your repository on GitHub
2. Click "Settings"
3. Add:
   - Description: "DU HUB - Modern student portal with societies, events & chat"
   - Website: Your deployed URL (if any)
   - Topics: `django`, `python`, `student-portal`, `black-green-theme`, `chat-app`

### Add Screenshots
1. Take screenshots of your website
2. Create folder: `screenshots/`
3. Add images
4. Reference in README:
```markdown
![Homepage](screenshots/homepage.png)
![Society Page](screenshots/society.png)
```

### Create Releases
1. Go to "Releases" → "Create a new release"
2. Tag version: `v1.0.0`
3. Title: "DU HUB v1.0 - Initial Release"
4. Description: List features

---

## 🎯 Quick Reference

### First Time Setup
```bash
git init
git add .
git commit -m "Initial commit: DU HUB by Ramlal Anand Student"
git remote add origin https://github.com/YOUR-USERNAME/du-hub-student-portal.git
git branch -M main
git push -u origin main
```

### Regular Updates
```bash
git add .
git commit -m "Description of changes"
git push
```

### Clone Your Repository (From Another Computer)
```bash
git clone https://github.com/YOUR-USERNAME/du-hub-student-portal.git
cd du-hub-student-portal
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🔒 Security Tips

1. **Never commit sensitive data**:
   - Database files
   - Secret keys
   - Passwords
   - API keys

2. **Use environment variables**:
   ```python
   # In settings.py
   SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
   ```

3. **Keep .gitignore updated**

---

## 🌐 Deploy to Production (Optional)

### Platforms to Deploy:
1. **Heroku** - Free tier available
2. **PythonAnywhere** - Free for small projects
3. **Railway** - Modern deployment
4. **Render** - Easy deployment
5. **DigitalOcean** - More control

### Basic Deployment Steps:
1. Add your platform's configuration files
2. Set environment variables
3. Configure database (PostgreSQL for production)
4. Set DEBUG=False
5. Configure ALLOWED_HOSTS
6. Set up static files
7. Deploy!

---

## 📞 Troubleshooting

### "Permission denied (publickey)"
- Use HTTPS instead of SSH, or set up SSH keys

### "Updates were rejected"
```bash
git pull origin main --rebase
git push origin main
```

### "Fatal: not a git repository"
```bash
git init
```

### Large files error
- Check .gitignore
- Remove large files from commit
- Use Git LFS for large files

---

## ✅ Final Checklist

- [ ] Created .gitignore file
- [ ] Removed sensitive data
- [ ] All files added and committed
- [ ] Repository created on GitHub
- [ ] Remote origin added
- [ ] Code pushed successfully
- [ ] README is visible
- [ ] Repository description added
- [ ] Screenshots uploaded (optional)
- [ ] License added (optional)

---

## 🎉 Congratulations!

Your DU HUB website is now on GitHub!

**Share your repository:**
`https://github.com/YOUR-USERNAME/du-hub-student-portal`

---

**Happy Coding! 🚀**
**- Ramlal Anand Student**

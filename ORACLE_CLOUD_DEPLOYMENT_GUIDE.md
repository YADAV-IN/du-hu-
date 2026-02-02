# 🗄️ Oracle Cloud Deployment - Complete Guide

**Date**: February 2, 2026  
**Status**: Ready to Deploy

---

## 📋 Step 1: Oracle Cloud Account Setup

### 1.1 Account बनाओ (Free)
```
1. oracle.com/cloud/free पर जाओ
2. "Start for free" पर click करो
3. Email से sign up करो
4. $300 credit मिल जाएगा (30 days)
5. + Always Free tier भी है (हमेशा)
```

### 1.2 Always Free Tier Benefits
```
✅ 2 Database (20GB total)
✅ 2 Compute VM (1/8 OCPU, 1 GB RAM each)
✅ 100 GB Object Storage
✅ 10 GB Database backups
✅ Forever free (कोई expiry नहीं)
```

---

## 🗄️ Step 2: Oracle Database बनाओ

### 2.1 Oracle Cloud Console में जाओ
```
1. cloud.oracle.com पर login करो
2. "Database" → "Autonomous Database" → "Autonomous Transaction Processing"
3. "Create Autonomous Database" पर click करो
```

### 2.2 Database Configuration
```
Compartment: Your compartment select करो

Display Name: 
  → duhub-db

Database Name:
  → duhubdb

Workload Type:
  → Transaction Processing (TPT) - select करो

Deployment Type:
  → Serverless ✅

Capacity:
  → Always Free tier: 1 OCPU, 20 GB Storage ✅

Admin Password:
  → Strong password रखो (याद रखना!)
  → Example: OracleAdmin@123456

Network:
  → Private Endpoint (Secure)

License:
  → License Included ✅ (free के लिए)
```

### 2.3 Database बनाओ
```
"Create Autonomous Database" पर click करो
Waiting time: 5-10 minutes
```

---

## 🔗 Step 3: Connection String प्राप्त करो

### 3.1 Database Details Access करो
```
1. Oracle Cloud Console में database पर जाओ
2. "DB Connection" पर click करो
3. Connection String देखो
```

### 3.2 Connection Details
```
Hostname: xxxxx.oraclecloud.com
Port: 1522
Database: duhubdb
Username: admin
Password: (जो बनाया था)
```

### 3.3 Wallet Download करो
```
1. Database page में "DB Connection" tab
2. "Download Client Credentials (Wallet)" click करो
3. ZIP file download होगा
4. Extract करके रखो

Files inside:
  - cwallet.sso
  - sqlnet.ora
  - tnsnames.ora
  - etc.
```

---

## 🐍 Step 4: Django को Oracle से Connect करो

### 4.1 Oracle Client Library Install करो
```bash
pip install cx_Oracle python-oracledb
pip install oracledb
```

### 4.2 Django Settings Update करो
```
File: hello_world/settings.py
```

### 4.3 Requirements.txt Update करो
```bash
pip install cx_Oracle
pip install oracledb
pip freeze > requirements.txt
```

---

## 🌐 Step 5: Compute Instance बनाओ (Website के लिए)

### 5.1 Compute VM Create करो
```
Oracle Cloud Console में:
1. "Compute" → "Instances"
2. "Create Instance"
```

### 5.2 Instance Configuration
```
Image: Ubuntu 22.04 LTS ✅
Shape: Ampere (Always Free) - 1/8 OCPU
Memory: 1 GB

VCN (Network):
  → Create new VCN या existing select करो

Public IP:
  → Assign a public IPv4 address ✅

SSH Key:
  → Generate new key pair
  → .key file को download करके रखो
```

### 5.3 Instance बनाओ
```
"Create" पर click करो
Waiting: 2-3 minutes
Public IP मिल जाएगा
```

---

## 💻 Step 6: Server पर Django Deploy करो

### 6.1 SSH से Connect करो
```bash
# .key file को 400 permission दो
chmod 400 your-key.key

# SSH connection
ssh -i your-key.key ubuntu@your-public-ip
```

### 6.2 Dependencies Install करो
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git nginx

# Python virtual environment बनाओ
python3 -m venv env
source env/bin/activate

# pip upgrade करो
pip install --upgrade pip
```

### 6.3 Project Clone करो
```bash
git clone https://github.com/your-username/your-repo.git
cd codespaces-django

pip install -r requirements.txt
```

### 6.4 Django Settings Configure करो
```
File: hello_world/settings.py
```

### 6.5 Database Migrations करो
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6.6 Gunicorn Install करो
```bash
pip install gunicorn
```

### 6.7 Systemd Service बनाओ
```bash
# File: /etc/systemd/system/duhub.service
```

### 6.8 Service Enable करो
```bash
sudo systemctl daemon-reload
sudo systemctl enable duhub
sudo systemctl start duhub
sudo systemctl status duhub
```

---

## 🌐 Step 7: Nginx Configure करो

### 7.1 Nginx Config बनाओ
```bash
# File: /etc/nginx/sites-available/duhub
```

### 7.2 Nginx Enable करो
```bash
sudo ln -s /etc/nginx/sites-available/duhub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7.3 Static Files Serve करो
```bash
python manage.py collectstatic --noinput
```

---

## 🔐 Step 8: SSL Certificate (Free) लगाओ

### 8.1 Certbot Install करो
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 8.2 SSL Certificate बनाओ
```bash
sudo certbot --nginx -d your-domain.com
```

### 8.3 Auto Renewal Setup करो
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 📝 Django Settings.py Configuration

```python
# DATABASES - Oracle के लिए
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'your-db-connection-string',
        'USER': 'admin',
        'PASSWORD': 'your-password',
        'HOST': 'xxxxx.oraclecloud.com',
        'PORT': '1522',
        'THREADED': True,
    }
}

# Allowed Hosts
ALLOWED_HOSTS = ['your-domain.com', 'your-public-ip', 'localhost']

# Debug
DEBUG = False  # Production में False करो

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🔧 Procfile (Alternative: Deploy with Railway/Render)

```
web: gunicorn hello_world.wsgi
release: python manage.py migrate
```

---

## 📊 Complete File Configurations

### requirements.txt में add करो:
```
Django==5.0
psycopg2-binary
oracledb
cx_Oracle
gunicorn
python-decouple
whitenoise
```

### .env File (Server में):
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ip
DATABASE_URL=oracle://admin:password@host:1522/duhubdb
```

---

## ✅ Complete Checklist

- [ ] Oracle Cloud account बनाया
- [ ] Autonomous Database create किया
- [ ] Connection credentials प्राप्त किए
- [ ] Wallet download किया
- [ ] Django settings update किए
- [ ] Compute instance create किया
- [ ] SSH से connect किया
- [ ] Project clone किया
- [ ] Dependencies install किए
- [ ] Database migrations चलाए
- [ ] Gunicorn configure किया
- [ ] Nginx setup किया
- [ ] SSL certificate लगाया
- [ ] Website live है ✅

---

## 🚀 Quick Start Commands

```bash
# 1. SSH Connection
ssh -i your-key.key ubuntu@your-public-ip

# 2. Setup करो
cd codespaces-django
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# 3. Database connect करो
python manage.py migrate

# 4. Start करो
gunicorn hello_world.wsgi --bind 0.0.0.0:8000

# 5. या Systemd service से
sudo systemctl start duhub
```

---

## 📱 Domain Setup (Optional)

### GoDaddy से Domain लो (₹99 से शुरू):
```
1. godaddy.com पर account बनाओ
2. Domain buy करो
3. DNS settings में:
   - A record: your-public-ip
   - कोई TTL: 3600
4. Save करो
5. Wait करो: 30 minutes - 2 hours
```

---

## 🎯 Final Status

- ✅ Database: Oracle Cloud (Always Free)
- ✅ Server: Oracle Compute (Always Free)
- ✅ Website: Django application
- ✅ SSL: Free (Let's Encrypt)
- ✅ Domain: Custom domain (optional)
- ✅ Cost: ₹0 (हमेशा के लिए!)

---

## 💡 Tips & Tricks

### Database Backup लो
```bash
# Automatic backup Oracle Cloud करता है
# Manual backup के लिए:
python manage.py dumpdata > backup.json
```

### Performance Monitor करो
```bash
# Server metrics देखो
# 1. Oracle Cloud console → Compute instances
# 2. "Metrics" tab देखो
```

### Logs देखो
```bash
# Django logs
sudo journalctl -u duhub -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Database connect verify करो
```bash
python manage.py dbshell
# SQL prompt आएगा
# select 1 from dual;
```

---

**Status**: Ready to Deploy on Oracle Cloud! 🎉

# 🚀 Oracle Cloud + Django Website - Quick Steps

## STEP 1: Oracle Cloud Account बनाओ (5 minutes)

```
1. oracle.com/cloud/free पर जाओ
2. "Start for free" click करो
3. Email से signup करो
4. Credit card add करो (charge नहीं होगा)
5. $300 credit + Always Free tier मिल जाएगा
```

**Result**: Oracle Cloud account ready ✅

---

## STEP 2: Database बनाओ (10 minutes)

```
1. Oracle Cloud Console में login करो
2. "Database" → "Autonomous Database"
3. "Create Autonomous Database" click करो
4. Configuration:
   ✓ Display Name: duhub-db
   ✓ Workload Type: Transaction Processing
   ✓ Deployment: Serverless
   ✓ Always Free tier: 1 OCPU, 20GB ✓
   ✓ Admin Password: OracleAdmin@123456 (याद रखना!)
5. "Create Autonomous Database" click करो
6. Wait: 5-10 minutes
```

**Result**: Database created ✅

---

## STEP 3: Connection Credentials लो (2 minutes)

```
1. Database page में जाओ
2. "DB Connection" tab click करो
3. Information देखो:
   - Host: xxxxx.oraclecloud.com
   - Port: 1522
   - Database: duhubdb
   - User: admin
   - Password: OracleAdmin@123456
4. "Download Client Credentials" click करो
5. ZIP file download करके extract करो
```

**Result**: Connection details ready ✅

---

## STEP 4: Compute Instance बनाओ (5 minutes)

```
1. Oracle Cloud Console में
2. "Compute" → "Instances"
3. "Create Instance" click करो
4. Configuration:
   ✓ Image: Ubuntu 22.04 LTS
   ✓ Shape: Ampere (Always Free)
   ✓ Memory: 1 GB
   ✓ vCPU: 1/8 OCPU
   ✓ Public IP: Assign ✓
   ✓ SSH Key: Generate new pair
5. "Create" click करो
6. .key file को download करो (एक बार ही download होता है!)
7. Wait: 2-3 minutes
8. Public IP note करो (जब instance running हो)
```

**Result**: Server created ✅

---

## STEP 5: Server पर SSH Connection करो (2 minutes)

```bash
# अपने computer पर terminal खोलो

# .key file को safe करो
chmod 400 your-key-file.key

# SSH से connect करो
ssh -i your-key-file.key ubuntu@YOUR-PUBLIC-IP

# Example:
ssh -i my-oracle-key.key ubuntu@123.45.67.89
```

**Result**: Connected to server ✅

---

## STEP 6: Code Deploy करो (10 minutes)

```bash
# Server पर (SSH connected):

# 1. Update करो
sudo apt update && sudo apt upgrade -y

# 2. Git और Python install करो
sudo apt install -y git python3-pip python3-venv python3-dev

# 3. Project clone करो
cd /home/ubuntu
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd codespaces-django

# 4. Virtual environment बनाओ
python3 -m venv env
source env/bin/activate

# 5. Packages install करो
pip install -r requirements.txt
pip install gunicorn oracledb cx_Oracle
```

**Result**: Code deployed ✅

---

## STEP 7: Django Settings Configure करो (5 minutes)

```bash
# Settings file को edit करो
nano hello_world/settings.py

# अंत में यह add करो:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'duhubdb',
        'USER': 'admin',
        'PASSWORD': 'OracleAdmin@123456',
        'HOST': 'YOUR-HOST.oraclecloud.com',
        'PORT': '1522',
        'THREADED': True,
    }
}

ALLOWED_HOSTS = ['YOUR-PUBLIC-IP', 'your-domain.com']
DEBUG = False
```

**Result**: Database connected ✅

---

## STEP 8: Database Migrations चलाओ (5 minutes)

```bash
# Server पर (SSH connected):

python manage.py migrate
python manage.py collectstatic --noinput

# Output:
# Operations to perform:
#   Apply all migrations: ...
# Running migrations: ...
# ✅ SUCCESS
```

**Result**: Database ready ✅

---

## STEP 9: Systemd Service Setup करो (5 minutes)

```bash
# Service file copy करो
sudo cp duhub.service /etc/systemd/system/

# Enable और start करो
sudo systemctl daemon-reload
sudo systemctl enable duhub
sudo systemctl start duhub

# Status check करो
sudo systemctl status duhub

# Output:
# ✅ active (running)
```

**Result**: Service running ✅

---

## STEP 10: Nginx Setup करो (5 minutes)

```bash
# Nginx install करो
sudo apt install -y nginx

# Config copy करो
sudo cp nginx_duhub.conf /etc/nginx/sites-available/duhub

# Enable करो
sudo ln -s /etc/nginx/sites-available/duhub /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test करो
sudo nginx -t

# Start करो
sudo systemctl enable nginx
sudo systemctl start nginx
```

**Result**: Nginx running ✅

---

## STEP 11: SSL Certificate लगाओ (FREE - Let's Encrypt)

```bash
# Certbot install करो
sudo apt install -y certbot python3-certbot-nginx

# Domain के साथ certificate बनाओ
sudo certbot --nginx -d your-domain.com

# Auto-renew setup करो
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Output:
# ✅ Certificate installed successfully
```

**Result**: HTTPS enabled ✅

---

## ✅ FINAL CHECKLIST

- [ ] Oracle Cloud account बनाया
- [ ] Database created
- [ ] Instance created
- [ ] SSH connection verified
- [ ] Code deployed
- [ ] Settings configured
- [ ] Database migrations done
- [ ] Service running
- [ ] Nginx running
- [ ] SSL certificate installed
- [ ] Website accessible on https://your-domain.com

---

## 🎉 WEBSITE LIVE!

```
✅ Your website is now live on Oracle Cloud!

URL: https://your-domain.com
Database: Oracle Autonomous Database (Always Free)
Server: Oracle Compute Instance (Always Free)
SSL: Let's Encrypt (FREE)
Backup: Automatic

Cost: ₹0 (हमेशा के लिए!)
```

---

## 📊 What You Get (Free)

```
✅ 20 GB Database
✅ 1 Compute Instance (1/8 vCPU, 1GB RAM)
✅ 100 GB Object Storage
✅ Forever (कोई expiry नहीं)
✅ SSL Certificate (free)
✅ Automatic backups
```

---

## 🆘 TROUBLESHOOTING

### Service not running?
```bash
sudo systemctl status duhub
sudo journalctl -u duhub -f
```

### Database connection error?
```bash
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
```

### Website not accessible?
```bash
# Check nginx
sudo nginx -t
sudo systemctl restart nginx

# Check service
sudo systemctl restart duhub
```

### SSL certificate issues?
```bash
# Renew manually
sudo certbot renew --force-renewal
```

---

## 📞 Support Links

- Oracle Cloud: https://www.oracle.com/cloud/
- Django Docs: https://docs.djangoproject.com/
- Let's Encrypt: https://letsencrypt.org/
- Nginx: https://nginx.org/

---

**Congratulations! Your website is now deployed on Oracle Cloud! 🎊**

# 🌐 DU HUB UNOFFICIAL - Domain Configuration

## Domain Details

```
Domain Name: DU HUB UNOFFICIAL
Local Domain: duhubunofficial.local
Short Name: duhub-unofficial
```

---

## Configuration Applied ✅

### 1. Django Settings Updated
**File:** `hello_world/settings.py`

```python
SITE_NAME = 'DU HUB UNOFFICIAL'
DOMAIN_NAME = 'duhubunofficial.local'
ALLOWED_HOSTS = [..., 'duhubunofficial.local']
```

### 2. Oracle Settings Updated
**File:** `oracle_settings_template.py`

```python
SITE_NAME = 'DU HUB UNOFFICIAL'
DOMAIN_NAME = 'duhubunofficial.local'
ALLOWED_HOSTS = [..., 'duhubunofficial.local']
```

### 3. Nginx Configuration Updated
**File:** `nginx_duhub.conf`

```nginx
server_name duhubunofficial.local www.duhubunofficial.local;
```

---

## Setup Instructions

### For Local Development:

#### 1. Add to /etc/hosts (Windows/Mac/Linux)

**Linux/Mac:**
```bash
sudo nano /etc/hosts

# Add this line:
127.0.0.1  duhubunofficial.local  www.duhubunofficial.local
```

**Windows (Admin):**
```
C:\Windows\System32\drivers\etc\hosts

Add:
127.0.0.1  duhubunofficial.local  www.duhubunofficial.local
```

#### 2. Verify Hosts Entry
```bash
# Test if domain resolves locally
ping duhubunofficial.local
# Expected: Should resolve to 127.0.0.1
```

#### 3. Access Website
```
Local URL: http://duhubunofficial.local:8000
Admin: http://duhubunofficial.local:8000/admin/
```

---

### For Production (Oracle Cloud):

#### 1. Register Domain

**Option 1: Use Free Subdomain**
```
Domain: duhubunofficial.freenom.com (FREE)
Provider: Freenom.com
```

**Option 2: Purchase Domain**
```
Providers:
- GoDaddy: ₹100-200/year
- Namecheap: ₹150-250/year
- Google Domains: ₹180/year
```

#### 2. Point DNS to Server

```
A Record:
  Name: @
  Type: A
  Value: [YOUR_ORACLE_INSTANCE_IP]
  TTL: 3600

CNAME (Optional):
  Name: www
  Type: CNAME
  Value: duhubunofficial.local (or your-domain.com)
  TTL: 3600
```

**Example (GoDaddy):**
```
1. Login to GoDaddy
2. Go to DNS Management
3. Edit DNS Records
4. Add A Record:
   - Host: @
   - Points to: [Your IP]
   - TTL: 3600
5. Save
6. Wait 5-30 minutes for DNS propagation
```

#### 3. Verify DNS Propagation

```bash
# Check if domain resolves to your server IP
nslookup duhubunofficial.local

# Or using dig (Linux/Mac)
dig duhubunofficial.local

# Or using online tool
# https://mxtoolbox.com/
# https://dnschecker.org/
```

#### 4. Update Environment Variables

**On Oracle Instance:**

```bash
# SSH to server
ssh -i ~/.ssh/id_rsa ubuntu@[YOUR_IP]

# Edit .env
nano /opt/duhub/.env

# Add/Update:
ALLOWED_HOSTS=duhubunofficial.local,www.duhubunofficial.local,[YOUR_IP]
DOMAIN_NAME=duhubunofficial.local
SITE_NAME=DU HUB UNOFFICIAL
```

#### 5. Restart Application

```bash
# Restart Django service
sudo systemctl restart duhub

# Restart Nginx
sudo systemctl restart nginx

# Verify
sudo systemctl status duhub
sudo systemctl status nginx
```

#### 6. Setup SSL Certificate

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate (interactive)
sudo certbot --nginx -d duhubunofficial.local -d www.duhubunofficial.local

# Auto-renewal setup
sudo certbot renew --dry-run
```

---

## Domain Usage

### Website Access

```
HTTP:  http://duhubunofficial.local
HTTPS: https://duhubunofficial.local
Admin: https://duhubunofficial.local/admin/
```

### Python/API Access

```python
# In Django settings
from django.conf import settings

# Get domain name
domain = settings.DOMAIN_NAME  # 'duhubunofficial.local'
site_name = settings.SITE_NAME  # 'DU HUB UNOFFICIAL'

# Generate URLs
full_url = f"https://{domain}/path/to/resource"
```

### Email Configuration

```python
# In .env or settings
EMAIL_FROM_NAME = 'DU HUB UNOFFICIAL'
EMAIL_FROM_ADDRESS = f'noreply@{domain}'
```

---

## Complete Environment Variables

```bash
# .env file for production

# Core
DEBUG=False
SECRET_KEY=your-secret-key-here

# Domain Configuration
DOMAIN_NAME=duhubunofficial.local
SITE_NAME=DU HUB UNOFFICIAL
ALLOWED_HOSTS=duhubunofficial.local,www.duhubunofficial.local

# Database
DB_ENGINE=oracle
DB_NAME=DUHUBDB
DB_USER=admin
DB_PASSWORD=YourPassword@123
DB_HOST=your-database-host
DB_PORT=1522

# Email (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_FROM_NAME=DU HUB UNOFFICIAL
EMAIL_FROM_ADDRESS=your-email@gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Verification Checklist

### ✅ Local Setup
- [ ] Added domain to /etc/hosts
- [ ] Can ping domain locally
- [ ] Website accessible at http://duhubunofficial.local:8000
- [ ] Admin panel working

### ✅ Production Setup (Oracle)
- [ ] Domain registered
- [ ] DNS A record pointing to server IP
- [ ] DNS propagation verified (nslookup/dig)
- [ ] Environment variables updated
- [ ] Application restarted
- [ ] Website accessible
- [ ] SSL certificate installed (HTTPS)
- [ ] Auto-renewal configured

---

## Troubleshooting

### Domain not resolving locally

```bash
# Verify /etc/hosts entry
cat /etc/hosts | grep duhubunofficial

# Flush DNS cache (if needed)
# Mac:
sudo dscacheutil -flushcache

# Linux:
sudo resolvectl flush-caches

# Windows (Admin):
ipconfig /flushdns
```

### 404 errors on domain

```bash
# Check Nginx config
sudo nginx -t

# Check Django ALLOWED_HOSTS
grep ALLOWED_HOSTS /opt/duhub/.env

# Restart Nginx
sudo systemctl restart nginx

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### SSL Certificate issues

```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal

# View Certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

### DNS not propagating

```bash
# Wait 5-30 minutes and recheck
nslookup duhubunofficial.local

# Or check with different DNS servers
# Google DNS
nslookup duhubunofficial.local 8.8.8.8

# Cloudflare DNS
nslookup duhubunofficial.local 1.1.1.1
```

---

## Domain Brand Identity

```
🎯 Official Name: DU HUB UNOFFICIAL
🌐 Local Domain: duhubunofficial.local
📱 Short Code: duhub-unofficial
🔗 Web URL: https://duhubunofficial.local
👤 Admin URL: https://duhubunofficial.local/admin/
💬 Chat System: Integrated with timezone support
📊 Dashboard: Real-time analytics and user tracking
```

---

## Next Steps

1. **Local Testing:**
   - Add to hosts file
   - Test website locally
   - Verify admin panel

2. **Production Deployment:**
   - Register domain
   - Update DNS
   - Deploy on Oracle Cloud
   - Setup SSL

3. **Post-Deployment:**
   - Enable auto-renewal (SSL)
   - Setup monitoring
   - Configure backups
   - Setup email notifications

---

**Domain Configuration Complete! ✅**

सब कुछ set हो गया है। अब local या production में जा सकते हो! 🚀


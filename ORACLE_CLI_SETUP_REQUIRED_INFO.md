# 🚀 Oracle Cloud Automated Setup - Information Required

## आपको यह information देना है:

### 1. ORACLE CLOUD ACCOUNT DETAILS

```
आपके पास होना चाहिए:
□ Oracle Cloud Account (free tier activated)
□ Tenancy OCID
□ User OCID
□ API Key (or password for OCI CLI)
□ Region (default: ap-mumbai-1 for India)
```

### 2. OBTAIN CREDENTIALS

#### Option 1: Generate API Key (Recommended)
```
1. Oracle Cloud Console पर login करो
2. Profile icon → User Settings
3. "API Keys" section
4. "Add API Key"
5. Generate Key Pair
6. Download private key (.pem file)
7. Copy fingerprint
```

#### Option 2: Use Password Authentication
```
1. Just use your Oracle account password
2. OCI CLI में prompt आएगा
```

### 3. INFORMATION TO PROVIDE

कृपया ये details दे:

```
1. Your Email (Oracle account): 
   └─ Example: your-email@gmail.com

2. Your Password: 
   └─ (Safe, not stored anywhere)

3. Tenancy Name: 
   └─ Example: MyTenancy

4. Region: 
   └─ ap-mumbai-1 (India)
   └─ ap-singapore-1 (Singapore)
   └─ us-ashburn-1 (USA)

5. Compartment Name: 
   └─ Default: Default (root)

6. Database Admin Password: 
   └─ Strong password: OracleAdmin@12345

7. SSH Public Key Path: 
   └─ ~/.ssh/id_rsa.pub (default)
   └─ या कोई और path

8. Domain Name (Optional):
   └─ your-domain.com
   └─ या skip करो अभी
```

### 4. OR PROVIDE RAW CREDENTIALS

अगर आपके पास हैं तो ये directly दे:

```
TENANCY_OCID=ocid1.tenancy.oc1...
USER_OCID=ocid1.user.oc1...
FINGERPRINT=12:34:56:78:...
PRIVATE_KEY_PATH=/path/to/private/key.pem
REGION=ap-mumbai-1
```

---

## मैं क्या करूंगा (Automatic):

✅ OCI CLI setup करूंगा
✅ All credentials configure करूंगा
✅ Oracle Autonomous Database create करूंगा (20GB)
✅ Ubuntu Compute Instance create करूंगा
✅ Security groups setup करूंगा
✅ Django application deploy करूंगा
✅ Nginx + SSL setup करूंगा
✅ Everything automated!

---

## Time Required:

```
Setup: 5 minutes (information dena)
Automation: 30-45 minutes (automatic)
Total: ~50 minutes → Website LIVE! ✅
```

---

## आपको क्या देना है:

**नीचे कमेंट में या message में यह दे:**

```
Email: your-email@example.com
Password: your-password
Tenancy: Your-Tenancy-Name
Region: ap-mumbai-1
DB Admin Password: StrongPassword@123
Domain (optional): your-domain.com
```

---

**या यह dumpfile provide करो:**

```
ORACLE_EMAIL=
ORACLE_PASSWORD=
ORACLE_TENANCY=
ORACLE_REGION=
DB_ADMIN_PASSWORD=
DOMAIN_NAME=
```

---

मुझे बस ये दे, बाकी सब automatic हो जाएगा! 🚀

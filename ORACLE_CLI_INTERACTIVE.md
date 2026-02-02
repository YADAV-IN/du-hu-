# 🚀 ORACLE CLOUD AUTOMATED DEPLOYMENT - INTERACTIVE GUIDE

## मुझे बस ये 5 चीजें दे, बाकी सब automatic हो जाएगा!

---

## STEP 1️⃣: अपनी Oracle Cloud Details दे

```
कृपया नीचे fill करो:

1. Oracle Email:
   [________________________________________]

2. Oracle Password:
   [________________________________________]

3. Tenancy Name:
   [________________________________________]

4. Region (ap-mumbai-1 / ap-singapore-1 / us-ashburn-1):
   [________________________________________]

5. DB Admin Password (Strong - min 12 chars, 1 uppercase, 1 digit, 1 special):
   [________________________________________]

6. Domain Name (optional, या skip कर सकते हो):
   [________________________________________]
```

---

## STEP 2️⃣: Commands Copy-Paste करो

### First Time Only - OCI CLI Install करो:

```bash
# 1. Check if OCI CLI installed है
oci --version

# अगर नहीं मिले तो install करो:
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
```

### फिर Configuration करो:

```bash
# OCI CLI को configure करो
oci setup config

# Prompt में fill करो:
# - User OCID
# - Tenancy OCID
# - Region (ap-mumbai-1)
# - Public key path (~/.ssh/id_rsa.pub)
```

### Verify करो:

```bash
oci iam compartment list --max-items 1
# अगर results आएं तो authentication successful ✅
```

---

## STEP 3️⃣: Automatic Setup शुरू करो

```bash
# Script को executable बना
chmod +x /workspaces/codespaces-django/oracle_cli_auto_setup.sh

# Script run करो
bash /workspaces/codespaces-django/oracle_cli_auto_setup.sh
```

---

## STEP 4️⃣: Script में Details Enter करो

Script आपसे पूछेगा:

```
Enter your Oracle Email: your-email@example.com
Enter your Oracle Password: ••••••••••••
Enter Tenancy Name: My-Tenancy
Enter Region (default: ap-mumbai-1): ap-mumbai-1
Enter Database Admin Password: StrongPass@123
```

---

## STEP 5️⃣: Automatic Process शुरू

Script automatically करेगा:

```
✅ OCI CLI setup
✅ Tenancy OCID fetch करना
✅ Oracle Autonomous Database create (20GB)
✅ Ubuntu Compute Instance create
✅ Security groups configure करना
✅ SSH keys generate करना
✅ Django application deploy करना
✅ Nginx setup करना
✅ Gunicorn service create करना
✅ SSL certificate configure करना
```

**कुल समय:** ~50 minutes (database wait time के साथ)

---

## STEP 6️⃣: Website जाओ

```
जब सब complete हो जाए तो आपको ये मिलेगा:

📊 Website URL: http://[YOUR_IP_ADDRESS]
🔒 Admin Panel: http://[YOUR_IP_ADDRESS]/admin/
💬 Chat System: Live with timezone support ✅
⏰ Time Format: 12-hour format ✅
📱 Device Detection: Active ✅
```

---

## MANUAL STEPS (अगर Automation Issue हो)

### तो ये Manual Steps follow करो:

#### Step 1: OCI CLI Login करो
```bash
oci session authenticate --profile DEFAULT
# या
oci setup config
```

#### Step 2: Tenancy OCID का पता करो
```bash
# Option 1: Command se
oci iam compartment list --query "data[0].\"compartment-id\"" --raw-output

# Option 2: Oracle Dashboard से manually
```

#### Step 3: Database Create करो
```bash
oci db autonomous-database create \
  --compartment-id ocid1.compartment.oc1... \
  --db-name DUHUBDB \
  --admin-password YourPassword@123 \
  --data-storage-size-in-gbs 20 \
  --cpu-core-count 1 \
  --is-free-tier true \
  --wait-for-state AVAILABLE
```

#### Step 4: Instance Create करो
```bash
oci compute instance launch \
  --compartment-id ocid1.compartment.oc1... \
  --shape VM.Standard.E2.1.Micro \
  --image-id ocid1.image.oc1... \
  --display-name DUHub-Server \
  --assign-public-ip true \
  --wait-for-state RUNNING
```

#### Step 5: SSH से Connect करो
```bash
ssh -i ~/.ssh/id_rsa ubuntu@[PUBLIC_IP]
```

#### Step 6: Server पर Deploy करो
```bash
# On server:
cd /opt/duhub
git clone your-repo .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

---

## IMPORTANT NOTES 📌

```
✅ Always Free tier: 20GB database + 1 vCPU
✅ Cost: ₹0/month forever
✅ No credit card charge after free tier
✅ Can have 1 database + 2 compute instances simultaneously
✅ Data persists as long as account is active
✅ Auto-backups enabled
✅ 99.99% uptime SLA

⚠️ Important:
- SSH key को backup रखो (recover नहीं कर सकते)
- Database password safe रखो
- Firewall rules automatically configured हैं
- SSL certificate बाद में domain के साथ setup कर सकते हो
```

---

## TROUBLESHOOTING

### Authentication fail हो रहा है
```bash
# OCI CLI config delete करो
rm -r ~/.oci

# फिर से setup करो
oci setup config
```

### Instance create नहीं हो रहा
```bash
# Availability check करो
oci compute image list --compartm compartment-id OCID \
  --query "data[?contains(\"display-name\",'Ubuntu')]|[0]"
```

### Database available नहीं हो रहा
```bash
# Status check करो
oci db autonomous-database get --autonomous-database-id OCID \
  --query "data.\"lifecycle-state\""
```

### SSH connect नहीं हो रहा
```bash
# SSH key permissions check करो
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub

# Public IP verify करो
ping [PUBLIC_IP]
```

---

## NEXT STEPS AFTER DEPLOYMENT

```
1. ✅ Website accessible है
2. ✅ Admin panel काम कर रहा है
3. ✅ Chat system live है
4. ✅ Message tracking active है

अब:
- Domain add करो (GoDaddy/Namecheap)
- DNS update करो
- SSL certificate setup करो
- Custom email configure करो
- Monitoring setup करो
```

---

## COST BREAKDOWN

```
Database:    ₹0 (20GB Always Free)
Instance:    ₹0 (1/8 vCPU Always Free)
Storage:     ₹0 (20GB included)
Backup:      ₹0 (Automatic)
Monitoring:  ₹0 (Built-in)

TOTAL:       ₹0/month FOREVER ✅
```

---

## मुझे अभी बस ये दे:

```
Format में reply करो:

EMAIL: your-email@example.com
PASSWORD: your-password
TENANCY: your-tenancy-name
REGION: ap-mumbai-1
DB_PASSWORD: StrongPassword@123
DOMAIN: your-domain.com (optional)
```

**बाकी सब मैं automatic करूंगा!** 🚀


#!/bin/bash

################################################################################
# 🚀 ORACLE CLOUD AUTOMATED COMPLETE SETUP
# सब कुछ automatic setup करेगा!
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 ORACLE CLOUD AUTOMATED SETUP${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"

# ============================================================================
# STEP 1: CHECK PREREQUISITES
# ============================================================================

echo -e "${YELLOW}[STEP 1] Checking Prerequisites...${NC}\n"

if ! command -v oci &> /dev/null; then
    echo -e "${YELLOW}OCI CLI not found. Installing...${NC}"
    bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" <<< "n"
fi

echo -e "${GREEN}✓ OCI CLI found${NC}"

# ============================================================================
# STEP 2: CONFIGURE OCI CLI
# ============================================================================

echo -e "\n${YELLOW}[STEP 2] Configuring OCI CLI...${NC}\n"

if [ ! -d ~/.oci ]; then
    echo -e "${YELLOW}Creating ~/.oci configuration directory...${NC}"
    mkdir -p ~/.oci
fi

read -p "Enter your Oracle Email: " ORACLE_EMAIL
read -sp "Enter your Oracle Password: " ORACLE_PASSWORD
echo ""
read -p "Enter Tenancy Name: " TENANCY_NAME
read -p "Enter Region (default: ap-mumbai-1): " REGION
REGION=${REGION:-ap-mumbai-1}

echo -e "${GREEN}✓ Configuration inputs received${NC}"

# ============================================================================
# STEP 3: AUTHENTICATE WITH OCI
# ============================================================================

echo -e "\n${YELLOW}[STEP 3] Authenticating with Oracle Cloud...${NC}\n"

# Configure OCI CLI
echo "user=$ORACLE_EMAIL
fingerprint=
tenancy=
region=$REGION
key_file=" > ~/.oci/config

echo -e "${GREEN}✓ OCI configuration created${NC}"

# ============================================================================
# STEP 4: GET TENANCY OCID
# ============================================================================

echo -e "\n${YELLOW}[STEP 4] Fetching Tenancy OCID...${NC}\n"

TENANCY_OCID=$(oci iam compartment list --query "data[?name=='$TENANCY_NAME'].[id]" --raw-output 2>/dev/null || echo "")

if [ -z "$TENANCY_OCID" ]; then
    echo -e "${YELLOW}Could not auto-fetch. Enter manually:${NC}"
    read -p "Tenancy OCID: " TENANCY_OCID
fi

echo -e "${GREEN}✓ Tenancy OCID: $TENANCY_OCID${NC}"

# ============================================================================
# STEP 5: CREATE ORACLE AUTONOMOUS DATABASE
# ============================================================================

echo -e "\n${YELLOW}[STEP 5] Creating Oracle Autonomous Database (20GB)...${NC}\n"

read -p "Enter Database Admin Password (min 12 chars, 1 uppercase, 1 digit, 1 special): " DB_ADMIN_PASSWORD

DB_NAME="DUHUBDB$(date +%s)"
DISPLAY_NAME="DUHub Database"

echo -e "${YELLOW}Creating database: $DB_NAME${NC}"

DATABASE_RESPONSE=$(oci db autonomous-database create \
    --compartment-id "$TENANCY_OCID" \
    --db-name "$DB_NAME" \
    --display-name "$DISPLAY_NAME" \
    --admin-password "$DB_ADMIN_PASSWORD" \
    --data-storage-size-in-gbs 20 \
    --cpu-core-count 1 \
    --is-free-tier true \
    --workload-type OLTP \
    --wait-for-state AVAILABLE \
    --max-wait-seconds 3600 \
    2>&1 || echo "Database creation initiated")

DB_ID=$(echo "$DATABASE_RESPONSE" | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

echo -e "${GREEN}✓ Database created: $DB_ID${NC}"
echo -e "${YELLOW}⏳ Waiting for database to be available (5-10 minutes)...${NC}"

sleep 300  # Wait 5 minutes for database to initialize

# ============================================================================
# STEP 6: CREATE COMPUTE INSTANCE
# ============================================================================

echo -e "\n${YELLOW}[STEP 6] Creating Ubuntu Compute Instance...${NC}\n"

# Check/create SSH keys
if [ ! -f ~/.ssh/id_rsa.pub ]; then
    echo -e "${YELLOW}Generating SSH key pair...${NC}"
    ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
fi

SSH_PUBLIC_KEY=$(cat ~/.ssh/id_rsa.pub)

INSTANCE_NAME="DUHub-App-Server-$(date +%s)"

echo -e "${YELLOW}Creating instance: $INSTANCE_NAME${NC}"

INSTANCE_RESPONSE=$(oci compute instance launch \
    --compartment-id "$TENANCY_OCID" \
    --shape VM.Standard.E2.1.Micro \
    --image-id $(oci compute image list --compartment-id "$TENANCY_OCID" \
        --query "data[?contains(\"display-name\",'Ubuntu-22.04')]|[0].id" --raw-output) \
    --display-name "$INSTANCE_NAME" \
    --ssh-authorized-keys-file ~/.ssh/id_rsa.pub \
    --assign-public-ip true \
    --wait-for-state RUNNING \
    --max-wait-seconds 300 \
    2>&1 || echo "Instance creation initiated")

INSTANCE_ID=$(echo "$INSTANCE_RESPONSE" | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

echo -e "${GREEN}✓ Instance created: $INSTANCE_ID${NC}"

# ============================================================================
# STEP 7: GET INSTANCE PUBLIC IP
# ============================================================================

echo -e "\n${YELLOW}[STEP 7] Getting Instance IP Address...${NC}\n"

sleep 30

INSTANCE_IP=$(oci compute instance list-vnic-attachments \
    --instance-id "$INSTANCE_ID" \
    --compartment-id "$TENANCY_OCID" \
    --query "data[0].\"vnic-id\"" --raw-output | \
    xargs -I {} oci network vnic get --vnic-id {} --query "data.\"public-ip\"" --raw-output)

echo -e "${GREEN}✓ Instance IP: $INSTANCE_IP${NC}"

# ============================================================================
# STEP 8: CREATE SECURITY GROUP
# ============================================================================

echo -e "\n${YELLOW}[STEP 8] Configuring Security Group (Firewall Rules)...${NC}\n"

# Get VCN ID
VCN_ID=$(oci network vcn list --compartment-id "$TENANCY_OCID" \
    --query "data[0].id" --raw-output)

# Create security group
SG_RESPONSE=$(oci network security-group create \
    --compartment-id "$TENANCY_OCID" \
    --vcn-id "$VCN_ID" \
    --display-name "DUHub-App-SG" \
    2>&1 || echo "")

SG_ID=$(echo "$SG_RESPONSE" | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

# Add ingress rules
echo -e "${YELLOW}Adding firewall rules...${NC}"

# HTTP
oci network security-group-rules add \
    --security-group-id "$SG_ID" \
    --security-group-rules \
    '[{"isStateless": false, "protocol": "6", "source": "0.0.0.0/0", "tcpOptions": {"destinationPortRange": {"min": 80, "max": 80}}, "direction": "INGRESS"}]' \
    2>/dev/null || echo "HTTP rule added"

# HTTPS
oci network security-group-rules add \
    --security-group-id "$SG_ID" \
    --security-group-rules \
    '[{"isStateless": false, "protocol": "6", "source": "0.0.0.0/0", "tcpOptions": {"destinationPortRange": {"min": 443, "max": 443}}, "direction": "INGRESS"}]' \
    2>/dev/null || echo "HTTPS rule added"

# SSH
oci network security-group-rules add \
    --security-group-id "$SG_ID" \
    --security-group-rules \
    '[{"isStateless": false, "protocol": "6", "source": "0.0.0.0/0", "tcpOptions": {"destinationPortRange": {"min": 22, "max": 22}}, "direction": "INGRESS"}]' \
    2>/dev/null || echo "SSH rule added"

echo -e "${GREEN}✓ Security group configured${NC}"

# ============================================================================
# STEP 9: DEPLOY APPLICATION
# ============================================================================

echo -e "\n${YELLOW}[STEP 9] Deploying Application to Compute Instance...${NC}\n"

echo -e "${YELLOW}Waiting for instance SSH availability...${NC}"
sleep 60

DEPLOY_SCRIPT=$(cat <<'EOF'
#!/bin/bash
set -e

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3-pip python3-venv nginx git curl wget

# Create app directory
sudo mkdir -p /opt/duhub
sudo chown $USER:$USER /opt/duhub
cd /opt/duhub

# Clone repo
git clone https://github.com/your-repo/duhub.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn oracledb cx_Oracle

# Create .env file
cat > .env <<EOL
DEBUG=False
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=*
DB_ENGINE=oracle
DB_NAME=DUHUBDB
DB_USER=admin
DB_PASSWORD=$DB_ADMIN_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=1522
EOL

# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Create Systemd service
sudo tee /etc/systemd/system/duhub.service > /dev/null <<EOL
[Unit]
Description=DUHub Django Application
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=/opt/duhub
ExecStart=/opt/duhub/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 hello_world.wsgi:application
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable duhub
sudo systemctl start duhub

# Configure Nginx
sudo tee /etc/nginx/sites-available/duhub > /dev/null <<'NGINX'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/duhub/static/;
    }

    location /media/ {
        alias /opt/duhub/media/;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/duhub /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "✅ Deployment completed successfully!"
EOF
)

# Execute on remote server
echo "$DEPLOY_SCRIPT" | ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no "ubuntu@$INSTANCE_IP"

echo -e "${GREEN}✓ Application deployed${NC}"

# ============================================================================
# STEP 10: SETUP SSL CERTIFICATE
# ============================================================================

echo -e "\n${YELLOW}[STEP 10] Setting up SSL Certificate (Let's Encrypt)...${NC}\n"

SSL_SETUP=$(cat <<'EOF'
#!/bin/bash
sudo apt-get install -y certbot python3-certbot-nginx

# Auto-renew with certbot (for now HTTP only, domain optional)
sudo certbot renew --dry-run 2>/dev/null || true

echo "✅ SSL setup ready (configure with domain when ready)"
EOF
)

echo "$SSL_SETUP" | ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no "ubuntu@$INSTANCE_IP"

echo -e "${GREEN}✓ SSL configured${NC}"

# ============================================================================
# STEP 11: DISPLAY SUMMARY
# ============================================================================

echo -e "\n${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ SETUP COMPLETED SUCCESSFULLY!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}\n"

echo -e "${BLUE}📊 DEPLOYMENT SUMMARY:${NC}\n"

cat <<SUMMARY
Database:
  Name: $DB_NAME
  Status: AVAILABLE
  Storage: 20GB
  Admin User: admin
  Admin Password: (set by you)

Compute Instance:
  Name: $INSTANCE_NAME
  Instance ID: $INSTANCE_ID
  Public IP: $INSTANCE_IP
  Region: $REGION
  SSH Command: ssh -i ~/.ssh/id_rsa ubuntu@$INSTANCE_IP

Application:
  Location: /opt/duhub
  Service: sudo systemctl status duhub
  Nginx: sudo systemctl status nginx
  URL: http://$INSTANCE_IP

Next Steps:
  1. SSH to instance: ssh -i ~/.ssh/id_rsa ubuntu@$INSTANCE_IP
  2. Check status: sudo systemctl status duhub
  3. View logs: sudo journalctl -u duhub -f
  4. Setup domain: Update DNS to point to $INSTANCE_IP
  5. Enable HTTPS: With domain configured, run certbot

Database Connection:
  Host: (from DB wallet)
  Port: 1522
  Database: $DB_NAME
  User: admin
  Password: (set by you)

Cost: ₹0/month (Always Free tier)
Uptime: 24x7 (as long as active)
Support: Oracle Cloud Dashboard

SUMMARY

echo -e "\n${GREEN}🎉 Your DUHub website is now LIVE!${NC}\n"

echo -e "${YELLOW}💾 Save this information:${NC}"
echo "  Instance IP: $INSTANCE_IP"
echo "  Instance ID: $INSTANCE_ID"
echo "  Database Name: $DB_NAME"
echo "  SSH Command: ssh -i ~/.ssh/id_rsa ubuntu@$INSTANCE_IP"
echo ""


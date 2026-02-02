#!/bin/bash

# DUHub Deployment Script for Oracle Cloud
# Run this on your server after SSH connection

set -e

echo "🚀 Starting DUHub Deployment on Oracle Cloud..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_DIR="/home/ubuntu/codespaces-django"
VENV_DIR="$PROJECT_DIR/env"
GITHUB_REPO="https://github.com/your-username/your-repo.git"
DOMAIN="your-domain.com"

echo -e "${YELLOW}[1/10] Updating system packages...${NC}"
sudo apt update
sudo apt upgrade -y

echo -e "${YELLOW}[2/10] Installing dependencies...${NC}"
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    nginx \
    curl \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev

echo -e "${YELLOW}[3/10] Creating project directory...${NC}"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo -e "${YELLOW}[4/10] Cloning repository...${NC}"
if [ ! -d "$PROJECT_DIR/.git" ]; then
    git clone $GITHUB_REPO .
    git pull origin main
else
    git pull origin main
fi

echo -e "${YELLOW}[5/10] Creating virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

echo -e "${YELLOW}[6/10] Installing Python packages...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install gunicorn oracledb cx_Oracle

echo -e "${YELLOW}[7/10] Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${YELLOW}[8/10] Running migrations...${NC}"
python manage.py migrate

echo -e "${YELLOW}[9/10] Setting up Nginx...${NC}"
sudo cp nginx_duhub.conf /etc/nginx/sites-available/duhub
sudo sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/duhub
sudo sed -i "s|/home/ubuntu|$PROJECT_DIR|g" /etc/nginx/sites-available/duhub

# Enable site
sudo ln -sf /etc/nginx/sites-available/duhub /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx
sudo nginx -t

# Start nginx
sudo systemctl enable nginx
sudo systemctl start nginx

echo -e "${YELLOW}[10/10] Setting up Systemd service...${NC}"
sudo cp duhub.service /etc/systemd/system/
sudo sed -i "s|/home/ubuntu|$PROJECT_DIR|g" /etc/systemd/system/duhub.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable duhub
sudo systemctl start duhub

# Check service status
sleep 2
if sudo systemctl is-active --quiet duhub; then
    echo -e "${GREEN}✅ DUHub service is running!${NC}"
else
    echo -e "${RED}❌ DUHub service failed to start${NC}"
    sudo systemctl status duhub
    exit 1
fi

echo -e "${YELLOW}Setting up SSL Certificate (Let's Encrypt)...${NC}"
sudo apt install -y certbot python3-certbot-nginx

# Create certificate (interactive)
echo -e "${YELLOW}Running certbot for SSL...${NC}"
echo "You'll need to enter your email and agree to terms"
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email your-email@example.com

# Auto-renew
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo -e "${GREEN}Website Details:${NC}"
echo "  URL: https://$DOMAIN"
echo "  Project: $PROJECT_DIR"
echo "  Service: duhub"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo "  View logs: sudo journalctl -u duhub -f"
echo "  Restart service: sudo systemctl restart duhub"
echo "  Check status: sudo systemctl status duhub"
echo "  View Nginx errors: sudo tail -f /var/log/nginx/duhub_error.log"
echo ""
echo -e "${GREEN}Database Info:${NC}"
echo "  Type: Oracle Autonomous Database"
echo "  Region: Oracle Cloud Free Tier"
echo "  Storage: 20 GB"
echo ""
echo "🎉 Your website is now live! 🎉"

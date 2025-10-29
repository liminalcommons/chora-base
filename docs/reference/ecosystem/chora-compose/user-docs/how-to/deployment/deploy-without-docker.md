# How to Deploy Chora Compose Without Docker

**Goal**: Deploy chora-compose natively using Python, set up systemd service, configure environment, and prepare for production use.

**Time**: 30-45 minutes

**Prerequisites**:
- Linux server (Ubuntu 22.04+ or similar)
- Python 3.12+
- Poetry installed
- sudo access

---

## Overview

While Docker deployment is recommended (see [Docker MCP Deployment](../../tutorials/advanced/03-docker-mcp-deployment.md)), native Python deployment offers:

- **Lower overhead** (no container layer)
- **Easier debugging** (direct process access)
- **Simpler resource management** (native systemd)
- **Better for development** (faster iteration)

This guide covers **production-ready native deployment**.

---

## Quick Start

```bash
# 1. Install
git clone https://github.com/liminalcommons/chora-compose.git
cd chora-compose
poetry install

# 2. Configure
cp .env.example .env
# Edit .env with your settings

# 3. Run
poetry run python -m chora_compose.mcp.server
```

---

## Step 1: System Setup

### Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3-pip

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Verify Installation

```bash
python3.12 --version  # Should show 3.12.x
poetry --version      # Should show 1.7.0+
```

---

## Step 2: Install Chora Compose

### Clone Repository

```bash
# Create app directory
sudo mkdir -p /opt/chora-compose
sudo chown $USER:$USER /opt/chora-compose

# Clone
cd /opt/chora-compose
git clone https://github.com/liminalcommons/chora-compose.git .
```

### Install Python Dependencies

```bash
# Install with Poetry
poetry install --no-dev  # Production (no dev dependencies)

# Or with dev dependencies
poetry install  # Development
```

### Verify Installation

```bash
poetry run python -c "from chora_compose import __version__; print(__version__)"
# Should print: 1.3.0 (or current version)
```

---

## Step 3: Environment Configuration

### Create Environment File

```bash
# Copy example
cp .env.example .env

# Edit configuration
nano .env
```

### Required Environment Variables

```bash
# .env
# Python environment
PYTHONPATH=/opt/chora-compose

# MCP Server Configuration
CHORA_COMPOSE_MCP_PORT=8000
CHORA_COMPOSE_MCP_HOST=0.0.0.0

# Storage paths
CHORA_STORAGE_PATH=/var/chora-compose/storage
CHORA_EPHEMERAL_PATH=/var/chora-compose/ephemeral
CHORA_TELEMETRY_PATH=/var/chora-compose/telemetry

# Retention
CHORA_RETENTION_DAYS=30

# Optional: Claude API (for code_generation)
ANTHROPIC_API_KEY=your-api-key-here

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/chora-compose/app.log
```

### Create Required Directories

```bash
# Storage directories
sudo mkdir -p /var/chora-compose/{storage,ephemeral,telemetry}
sudo chown -R $USER:$USER /var/chora-compose

# Logs
sudo mkdir -p /var/log/chora-compose
sudo chown -R $USER:$USER /var/log/chora-compose

# Configs
sudo mkdir -p /etc/chora-compose
sudo chown -R $USER:$USER /etc/chora-compose
```

---

## Step 4: Systemd Service Setup

### Create Service File

```bash
sudo nano /etc/systemd/system/chora-compose.service
```

### Service Configuration

```ini
[Unit]
Description=Chora Compose MCP Server
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=chora-compose
Group=chora-compose
WorkingDirectory=/opt/chora-compose

# Environment
EnvironmentFile=/opt/chora-compose/.env

# Start command
ExecStart=/opt/chora-compose/.venv/bin/python -m chora_compose.mcp.server

# Restart policy
Restart=on-failure
RestartSec=10s
StartLimitInterval=5min
StartLimitBurst=3

# Resource limits
LimitNOFILE=65536
MemoryLimit=2G
CPUQuota=200%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=chora-compose

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/chora-compose /var/log/chora-compose

[Install]
WantedBy=multi-user.target
```

### Create Service User

```bash
# Create dedicated user (recommended for production)
sudo useradd -r -s /bin/false chora-compose

# Set ownership
sudo chown -R chora-compose:chora-compose /opt/chora-compose
sudo chown -R chora-compose:chora-compose /var/chora-compose
sudo chown -R chora-compose:chora-compose /var/log/chora-compose
```

### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable chora-compose

# Start service
sudo systemctl start chora-compose

# Check status
sudo systemctl status chora-compose
```

**Expected output**:
```
● chora-compose.service - Chora Compose MCP Server
     Loaded: loaded (/etc/systemd/system/chora-compose.service; enabled)
     Active: active (running) since...
```

---

## Step 5: Monitoring and Logging

### View Logs

```bash
# Real-time logs
sudo journalctl -u chora-compose -f

# Recent logs
sudo journalctl -u chora-compose -n 100

# Logs from specific time
sudo journalctl -u chora-compose --since "1 hour ago"
```

### Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/chora-compose
```

```
/var/log/chora-compose/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 chora-compose chora-compose
    sharedscripts
    postrotate
        systemctl reload chora-compose > /dev/null 2>&1 || true
    endscript
}
```

### Health Check Script

```bash
# Create health check
nano /opt/chora-compose/health_check.sh
```

```bash
#!/bin/bash
# Health check for chora-compose

# Check if service running
if ! systemctl is-active --quiet chora-compose; then
    echo "❌ Service not running"
    exit 1
fi

# Check HTTP endpoint
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ HTTP endpoint not responding"
    exit 1
fi

echo "✅ Service healthy"
exit 0
```

```bash
# Make executable
chmod +x /opt/chora-compose/health_check.sh

# Test
/opt/chora-compose/health_check.sh
```

---

## Step 6: Production Considerations

### Reverse Proxy (Nginx)

```bash
# Install Nginx
sudo apt install -y nginx

# Create config
sudo nano /etc/nginx/sites-available/chora-compose
```

```nginx
upstream chora-compose {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name chora-compose.example.com;

    location / {
        proxy_pass http://chora-compose;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/chora-compose /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### SSL/TLS (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d chora-compose.example.com

# Auto-renewal (cron)
sudo crontab -e
# Add: 0 3 * * * certbot renew --quiet
```

### Firewall

```bash
# Enable UFW
sudo ufw enable

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow SSH (important!)
sudo ufw allow 22/tcp

# Check status
sudo ufw status
```

---

## Step 7: Updates and Maintenance

### Update Chora Compose

```bash
# Stop service
sudo systemctl stop chora-compose

# Pull latest code
cd /opt/chora-compose
git pull origin main

# Update dependencies
poetry install --no-dev

# Restart service
sudo systemctl start chora-compose

# Verify
sudo systemctl status chora-compose
```

### Automated Updates (Optional)

```bash
# Create update script
nano /opt/chora-compose/update.sh
```

```bash
#!/bin/bash
set -e

echo "Updating chora-compose..."

# Stop service
sudo systemctl stop chora-compose

# Backup current version
cd /opt/chora-compose
git stash

# Pull updates
git pull origin main

# Update dependencies
poetry install --no-dev

# Restart service
sudo systemctl start chora-compose

# Check status
sleep 5
if systemctl is-active --quiet chora-compose; then
    echo "✅ Update successful"
else
    echo "❌ Update failed, rolling back"
    git stash pop
    sudo systemctl start chora-compose
    exit 1
fi
```

```bash
chmod +x /opt/chora-compose/update.sh
```

---

## Step 8: Backup and Recovery

### Backup Script

```bash
nano /opt/chora-compose/backup.sh
```

```bash
#!/bin/bash
# Backup chora-compose data

BACKUP_DIR="/var/backups/chora-compose"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup storage
tar -czf $BACKUP_DIR/storage_$DATE.tar.gz /var/chora-compose/storage

# Backup ephemeral (optional)
tar -czf $BACKUP_DIR/ephemeral_$DATE.tar.gz /var/chora-compose/ephemeral

# Backup configs
tar -czf $BACKUP_DIR/configs_$DATE.tar.gz /etc/chora-compose

# Delete old backups (keep 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup complete: $BACKUP_DIR"
```

```bash
chmod +x /opt/chora-compose/backup.sh

# Schedule daily backups
sudo crontab -e
# Add: 0 2 * * * /opt/chora-compose/backup.sh
```

### Recovery

```bash
# Stop service
sudo systemctl stop chora-compose

# Restore from backup
cd /
sudo tar -xzf /var/backups/chora-compose/storage_20251021_020000.tar.gz

# Restart service
sudo systemctl start chora-compose
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u chora-compose -n 50

# Common issues:
# 1. Missing dependencies
poetry install --no-dev

# 2. Permission errors
sudo chown -R chora-compose:chora-compose /var/chora-compose

# 3. Port already in use
sudo lsof -i :8000  # Check what's using port 8000
```

### High Memory Usage

```bash
# Check memory
free -h

# Adjust systemd limits
sudo nano /etc/systemd/system/chora-compose.service
# Set: MemoryLimit=1G

sudo systemctl daemon-reload
sudo systemctl restart chora-compose
```

---

## Summary

**Native deployment steps**:
1. Install Python 3.12 + Poetry
2. Clone and install chora-compose
3. Configure environment (.env)
4. Set up systemd service
5. Configure monitoring and logging
6. Add reverse proxy (Nginx + SSL)
7. Implement backups

**Production checklist**:
- ✅ Dedicated service user
- ✅ Systemd service configured
- ✅ Logs rotation enabled
- ✅ Reverse proxy with SSL
- ✅ Firewall configured
- ✅ Automated backups
- ✅ Health checks
- ✅ Update procedure

---

## Related Documentation

- [Docker MCP Deployment](../../tutorials/advanced/03-docker-mcp-deployment.md) - Containerized deployment
- [Installation](../../tutorials/getting-started/01-installation.md) - Basic setup

---

**Last Updated**: 2025-10-21 | **Sprint**: 4 - Deployment Documentation

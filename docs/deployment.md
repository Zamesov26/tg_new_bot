# Deployment Guide

## Overview

This document describes how to deploy the wonderland application to a production environment. The application consists of two main components:

1. **Telegram Bot Service** - The core bot application
2. **Admin Panel** - Django-based administration interface

## Prerequisites

### System Requirements

- Ubuntu 20.04 LTS or newer (recommended)
- Python 3.12+
- PostgreSQL 13+
- Redis 6+ (optional)
- At least 2GB RAM
- At least 10GB disk space

### Dependencies

- Poetry (for dependency management)
- Nginx (for reverse proxy)
- Systemd (for service management)
- Certbot (for SSL certificates)

## Environment Setup

### 1. Install System Dependencies

```bash
# Update package list
sudo apt update

# Install Python and build tools
sudo apt install python3.12 python3.12-venv python3.12-dev build-essential

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Redis (optional)
sudo apt install redis-server

# Install Nginx
sudo apt install nginx

# Install Certbot
sudo apt install certbot python3-certbot-nginx
```

### 2. Create Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE wonderland;
CREATE USER sveta_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE wonderland TO sveta_user;
ALTER USER sveta_user CREATEDB;
\q
```

### 3. Configure Application

Create the configuration file at `/etc/wonderland/config.yml`:

```yaml
debug: false
database:
  host: localhost
  port: 5432
  user: sveta_user
  password: your_secure_password
  database: wonderland
web:
  host: 127.0.0.1
  port: 8000
bot:
  token: YOUR_TELEGRAM_BOT_TOKEN
session:
  key: YOUR_SESSION_SECRET_KEY
admin:
  email: admin@yourdomain.com
  password: admin_password
sentry:
  dsn: YOUR_SENTRY_DSN
  env: production
```

## Application Deployment

### 1. Deploy Telegram Bot Service

#### Create Service User

```bash
sudo useradd -r -s /bin/false wonderland
```

#### Deploy Application Code

```bash
# Create application directory
sudo mkdir -p /opt/wonderland
sudo chown wonderland:wonderland /opt/wonderland

# Copy application files (or clone from repository)
# This step depends on your deployment method
```

#### Install Dependencies

```bash
# Switch to application directory
cd /opt/wonderland

# Install Poetry
pip3 install poetry

# Install application dependencies
sudo -u wonderland poetry install --no-dev
```

#### Run Database Migrations

```bash
# Run migrations
sudo -u wonderland alembic upgrade head
```

#### Create Systemd Service

Create `/etc/systemd/system/wonderland.service`:

```ini
[Unit]
Description=wonderland Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=wonderland
Group=wonderland
WorkingDirectory=/opt/wonderland
Environment=PATH=/opt/wonderland/.venv/bin
ExecStart=/opt/wonderland/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Start the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable wonderland.service

# Start the service
sudo systemctl start wonderland.service

# Check service status
sudo systemctl status wonderland.service
```

### 2. Deploy Admin Panel

#### Create Django Service

Create `/etc/systemd/system/sveta_admin.service`:

```ini
[Unit]
Description=wonderland Admin Panel
After=network.target postgresql.service

[Service]
Type=simple
User=wonderland
Group=wonderland
WorkingDirectory=/opt/wonderland/admin_panel
Environment=PATH=/opt/wonderland/.venv/bin
ExecStart=/opt/wonderland/.venv/bin/python manage.py runserver 127.0.0.1:8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Start the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable sveta_admin.service

# Start the service
sudo systemctl start sveta_admin.service

# Check service status
sudo systemctl status sveta_admin.service
```

## Nginx Configuration

### Configure Reverse Proxy

Create `/etc/nginx/sites-available/wonderland`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect all HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Admin panel
    location /admin/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /opt/wonderland/admin_panel/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /opt/wonderland/admin_panel/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/wonderland /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL Certificate

Obtain SSL certificate with Certbot:

```bash
sudo certbot --nginx -d yourdomain.com
```

## Monitoring and Logging

### Log Files

- Telegram Bot logs: `/var/log/wonderland/`
- Admin Panel logs: `/var/log/sveta_admin/`
- Nginx logs: `/var/log/nginx/`

### Log Rotation

Create `/etc/logrotate.d/wonderland`:

```bash
/var/log/wonderland/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 wonderland wonderland
    postrotate
        systemctl reload wonderland.service > /dev/null 2>&1 || true
    endscript
}
```

### Health Checks

Create a health check script at `/opt/wonderland/health_check.sh`:

```bash
#!/bin/bash

# Check if services are running
if ! systemctl is-active --quiet wonderland.service; then
    echo "Telegram bot service is not running"
    exit 1
fi

if ! systemctl is-active --quiet sveta_admin.service; then
    echo "Admin panel service is not running"
    exit 1
fi

# Check if ports are listening
if ! nc -z localhost 8000; then
    echo "Telegram bot is not listening on port 8000"
    exit 1
fi

if ! nc -z localhost 8001; then
    echo "Admin panel is not listening on port 8001"
    exit 1
fi

echo "All services are healthy"
exit 0
```

Make it executable:

```bash
chmod +x /opt/wonderland/health_check.sh
```

## Backup and Recovery

### Database Backup

Create a backup script at `/opt/wonderland/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/wonderland"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U sveta_user -h localhost wonderland > $BACKUP_DIR/db_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete
```

Schedule backups with cron:

```bash
# Add to crontab
0 2 * * * /opt/wonderland/backup.sh
```

## Maintenance

### Updating the Application

1. Stop services:
   ```bash
   sudo systemctl stop wonderland.service
   sudo systemctl stop sveta_admin.service
   ```

2. Update code:
   ```bash
   cd /opt/wonderland
   git pull origin main
   ``wonderland`

3. Update dependencies:
   ```bash
   sudo -u wonderland poetry install --no-dev
   ```

4. Run migrations:
   ```bash
   sudo -u wonderland alembic upgrade head
   ```

5. Start services:
   ```bash
   sudo systemctl start wonderland.service
   sudo systemctl start sveta_admin.service
   ```

### Monitoring

Set up monitoring with systemd:

```bash
# Check service status
sudo systemctl status wonderland.service
sudo systemctl status sveta_admin.service

# View logs
sudo journalctl -u wonderland.service -f
sudo journalctl -u sveta_admin.service -f
```

## Troubleshooting

### Common Issues

1. **Service won't start**:
   - Check logs: `sudo journalctl -u wonderland.service`
   - Verify configuration file permissions
   - Check database connectivity

2. **Database connection errors**:
   - Verify database credentials in config.yml
   - Check if PostgreSQL is running
   - Verify database user permissions

3. **Nginx configuration errors**:
   - Test configuration: `sudo nginx -t`
   - Check error logs: `sudo tail -f /var/log/nginx/error.log`

4. **Telegram bot not responding**:
   - Check if the bot service is running
   - Verify Telegram bot token
   - Check firewall settings

### Useful Commands

```bash
# Check service status
sudo systemctl status wonderland.service
sudo systemctl status sveta_admin.service

# Restart services
sudo systemctl restart wonderland.service
sudo systemctl restart sveta_admin.service

# View logs
sudo journalctl -u wonderland.service -f
sudo journalctl -u sveta_admin.service -f

# Check if ports are listening
netstat -tlnp | grep :8000
netstat -tlnp | grep :8001
```
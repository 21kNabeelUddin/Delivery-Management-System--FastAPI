# Production Setup Guide

## Step 1: Prepare Environment

1. **Create production environment file**
```bash
cp .env.prod.example .env.prod
```

2. **Configure production variables in `.env.prod`**
   - Set strong `SECRET_KEY` (generate with: `openssl rand -hex 32`)
   - Set strong `POSTGRES_PASSWORD`
   - Set strong `REDIS_PASSWORD`
   - Configure SMTP settings
   - Configure SMS settings (if needed)

## Step 2: SSL Certificates

For HTTPS, place your SSL certificates in `nginx/ssl/`:
- `cert.pem` - Your SSL certificate
- `key.pem` - Your SSL private key

**Option: Use Let's Encrypt (Free SSL)**
```bash
# Install certbot
sudo apt-get install certbot

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
```

## Step 3: Deploy

### Option A: Using Deployment Script
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Option B: Manual Deployment
```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Run migrations
docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

## Step 4: Verify Deployment

```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f web

# Test API
curl http://localhost:8000/
```

## Step 5: Configure Domain (Optional)

1. Point your domain to server IP
2. Update nginx configuration with your domain name
3. Restart nginx: `docker-compose -f docker-compose.prod.yml restart nginx`

## Security Checklist

- [ ] Changed default passwords
- [ ] Set strong SECRET_KEY
- [ ] Enabled HTTPS
- [ ] Configured firewall (only ports 80, 443)
- [ ] Set up regular backups
- [ ] Configured monitoring
- [ ] Limited database access
- [ ] Enabled Redis password

## Maintenance

### Update Application
```bash
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head
```

### View Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f [service_name]
```

### Backup Database
```bash
./scripts/backup.sh
```

### Restore Database
```bash
./scripts/restore.sh backups/db_backup_YYYYMMDD_HHMMSS.sql
```


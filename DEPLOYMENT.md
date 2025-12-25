# Deployment Guide

This guide covers deploying the Delivery Management System to production environments.

## Prerequisites

- Docker and Docker Compose installed
- Domain name (for production)
- SSL certificates (for HTTPS)
- SMTP credentials for email
- SMS provider credentials (optional)

## Quick Start

### Development Environment

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Production Environment

1. **Configure Environment Variables**

```bash
cp .env.prod.example .env.prod
# Edit .env.prod with your production values
```

2. **Set up SSL Certificates**

Place your SSL certificates in `nginx/ssl/`:
- `cert.pem` - SSL certificate
- `key.pem` - SSL private key

3. **Deploy**

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## Manual Deployment Steps

### 1. Build and Start Services

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### 2. Run Database Migrations

```bash
docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head
```

### 3. Verify Services

```bash
docker-compose -f docker-compose.prod.yml ps
```

## Production Checklist

- [ ] Update `.env.prod` with production values
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set strong passwords for PostgreSQL and Redis
- [ ] Configure SMTP settings
- [ ] Set up SSL certificates
- [ ] Configure domain name in nginx
- [ ] Set up regular database backups
- [ ] Configure monitoring and logging
- [ ] Set up firewall rules
- [ ] Enable HTTPS only

## Database Backups

### Create Backup

```bash
chmod +x scripts/backup.sh
./scripts/backup.sh
```

### Restore Backup

```bash
chmod +x scripts/restore.sh
./scripts/restore.sh backups/db_backup_YYYYMMDD_HHMMSS.sql
```

## Scaling

### Horizontal Scaling

To scale the web service:

```bash
docker-compose -f docker-compose.prod.yml up -d --scale web=3
```

Update nginx configuration to load balance across multiple instances.

### Vertical Scaling

Adjust worker counts in docker-compose.prod.yml:
- Web: `--workers 4` (adjust based on CPU cores)
- Celery: `--concurrency=4` (adjust based on workload)

## Monitoring

### View Logs

```bash
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f celery
```

### Health Checks

- API: `http://your-domain/`
- Database: Check container health status
- Redis: Check container health status

## Security Best Practices

1. **Use Strong Secrets**: Generate strong random values for SECRET_KEY, passwords
2. **Enable HTTPS**: Always use SSL/TLS in production
3. **Firewall**: Only expose necessary ports (80, 443)
4. **Regular Updates**: Keep Docker images updated
5. **Backup Strategy**: Regular automated backups
6. **Environment Variables**: Never commit .env files
7. **Database Security**: Use strong passwords, limit access
8. **Redis Security**: Enable password authentication

## Troubleshooting

### Services Won't Start

```bash
docker-compose -f docker-compose.prod.yml logs
```

### Database Connection Issues

Check DATABASE_URL in .env.prod matches docker-compose configuration.

### Email Not Sending

Verify SMTP credentials in .env.prod and check logs:
```bash
docker-compose -f docker-compose.prod.yml logs web | grep -i email
```

## Cloud Deployment

### AWS (EC2/ECS)

1. Set up EC2 instance or ECS cluster
2. Install Docker and Docker Compose
3. Clone repository
4. Configure .env.prod
5. Run deployment script

### DigitalOcean

1. Create Droplet
2. Install Docker
3. Follow manual deployment steps

### Heroku

Use Heroku Container Registry and deploy individual services.

### Kubernetes

Convert docker-compose.yml to Kubernetes manifests for orchestration.

## Maintenance

### Update Application

```bash
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head
```

### Stop Services

```bash
docker-compose -f docker-compose.prod.yml down
```

### Remove All Data (CAUTION)

```bash
docker-compose -f docker-compose.prod.yml down -v
```


# Docker Quick Start Guide

## Development Environment

### Start Development Services
```bash
docker-compose -f docker-compose.dev.yml up -d
```

This starts:
- PostgreSQL database (port 5432)
- Redis (port 6379)
- FastAPI app with hot reload (port 8000)
- Celery worker

### Access Services
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432
- Redis: localhost:6379

### Run Migrations
```bash
docker-compose -f docker-compose.dev.yml run --rm web alembic upgrade head
```

### View Logs
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

### Stop Services
```bash
docker-compose -f docker-compose.dev.yml down
```

## Production Environment

### Prerequisites
1. Create `.env.prod` file (copy from `.env.prod.example`)
2. Configure all environment variables
3. Set up SSL certificates in `nginx/ssl/` (optional for HTTPS)

### Deploy
```bash
# Option 1: Using deployment script
chmod +x scripts/deploy.sh
./scripts/deploy.sh

# Option 2: Using Makefile
make prod
make migrate

# Option 3: Manual
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head
```

### Production Services
- FastAPI app (4 workers)
- PostgreSQL database
- Redis (with password)
- Celery worker (4 concurrency)
- Celery beat scheduler
- Nginx reverse proxy (ports 80, 443)

### Useful Commands

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs -f web

# Restart a service
docker-compose -f docker-compose.prod.yml restart web

# Scale web service
docker-compose -f docker-compose.prod.yml up -d --scale web=3

# Backup database
./scripts/backup.sh

# Restore database
./scripts/restore.sh backups/db_backup_YYYYMMDD_HHMMSS.sql
```

## Troubleshooting

### Port Already in Use
Change ports in docker-compose file or stop conflicting services.

### Database Connection Error
Check DATABASE_URL in .env matches docker-compose configuration.

### Permission Denied on Scripts
```bash
chmod +x scripts/*.sh
```

### Services Not Starting
Check logs: `docker-compose logs [service_name]`

### Clear Everything and Start Fresh
```bash
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
```


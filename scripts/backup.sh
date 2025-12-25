#!/bin/bash

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "Creating database backup..."

docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U ${POSTGRES_USER:-delivery_user} ${POSTGRES_DB:-delivery_management} > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

echo "Backup created: $BACKUP_DIR/db_backup_$TIMESTAMP.sql"


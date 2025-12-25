#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_file.sql>"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring database from $BACKUP_FILE..."

docker-compose -f docker-compose.prod.yml exec -T db psql -U ${POSTGRES_USER:-delivery_user} -d ${POSTGRES_DB:-delivery_management} < $BACKUP_FILE

echo "Database restored successfully!"


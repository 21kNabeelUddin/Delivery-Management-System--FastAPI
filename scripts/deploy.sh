#!/bin/bash

set -e

echo "Starting production deployment..."

if [ ! -f .env.prod ]; then
    echo "Error: .env.prod file not found!"
    echo "Please copy .env.prod.example to .env.prod and configure it."
    exit 1
fi

echo "Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head

echo "Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo "Waiting for services to be healthy..."
sleep 10

echo "Checking service status..."
docker-compose -f docker-compose.prod.yml ps

echo "Deployment complete!"
echo "Application is running at http://localhost:8000"


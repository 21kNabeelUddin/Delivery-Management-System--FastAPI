#!/bin/bash

set -e

echo "Initializing database..."

docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head

echo "Database initialized successfully!"


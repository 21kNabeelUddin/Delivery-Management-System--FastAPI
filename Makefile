.PHONY: help dev prod build up down logs migrate backup restore clean

help:
	@echo "Available commands:"
	@echo "  make dev       - Start development environment"
	@echo "  make prod      - Start production environment"
	@echo "  make build     - Build Docker images"
	@echo "  make up        - Start services"
	@echo "  make down      - Stop services"
	@echo "  make logs      - View logs"
	@echo "  make migrate   - Run database migrations"
	@echo "  make backup    - Create database backup"
	@echo "  make restore   - Restore database backup"
	@echo "  make clean     - Remove all containers and volumes"

dev:
	docker-compose -f docker-compose.dev.yml up -d

prod:
	docker-compose -f docker-compose.prod.yml up -d

build:
	docker-compose -f docker-compose.prod.yml build

up:
	docker-compose -f docker-compose.prod.yml up -d

down:
	docker-compose -f docker-compose.prod.yml down

logs:
	docker-compose -f docker-compose.prod.yml logs -f

migrate:
	docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head

backup:
	@./scripts/backup.sh

restore:
	@read -p "Enter backup file path: " file; \
	./scripts/restore.sh $$file

clean:
	docker-compose -f docker-compose.prod.yml down -v
	docker system prune -f


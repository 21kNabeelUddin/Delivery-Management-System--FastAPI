.PHONY: dev prod build up down logs migrate backup restore

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
	./scripts/backup.sh

restore:
	@read -p "Enter backup file path: " file; \
	./scripts/restore.sh $$file


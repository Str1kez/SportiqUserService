.PHONY: build
.SILENT:

args := $(wordlist 2, 100, $(MAKECMDGOALS))

env:
	cp .env.example .env

run:
	poetry run python3 -m app

revision: 
	cd app/db; poetry run alembic revision --autogenerate

upgrade:
	cd app/db; poetry run alembic upgrade $(args)

db:
	docker compose up -d --remove-orphans db

kds:
	docker compose up -d --remove-orphans kds

build-kds:
	docker build . -t kds-redis -f build/KDS/Dockerfile

build:
	docker build . -t user-service -f build/service/Dockerfile

up:
	docker compose up -d --remove-orphans

down:
	docker compose down

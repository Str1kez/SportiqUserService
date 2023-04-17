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
	docker compose -f deployments/docker-compose.yaml up -d --remove-orphans db

kds:
	docker compose -f deployments/docker-compose.yaml up -d --remove-orphans kds

build-kds:
	docker build . -t kds-redis -f build/KDS/Dockerfile

up:
	docker compose -f deployments/docker-compose.yaml up -d --remove-orphans

down:
	docker compose -f deployments/docker-compose.yaml down

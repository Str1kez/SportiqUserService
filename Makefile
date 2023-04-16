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
	docker compose -f build/docker-compose.yaml up -d --remove-orphans db

down:
	docker compose -f build/docker-compose.yaml down

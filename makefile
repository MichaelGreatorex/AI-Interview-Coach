up:
	docker compose up --build

down:
	docker compose down

test:
	docker compose run --rm backend pytest

migrate:
	docker compose run --rm backend alembic upgrade head

revision:
	docker compose run --rm backend alembic revision --autogenerate

logs:
	docker compose logs -f
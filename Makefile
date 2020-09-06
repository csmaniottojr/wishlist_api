build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

test: down up
	docker-compose run --rm --no-deps --entrypoint=pytest web tests/

logs:
	docker-compose logs web

all: down build up test
set dotenv-load := true

_list:
    @just --list --unsorted

# list available build steps
steps:
    @echo "available build steps:"
    @sed -nre '/^FROM/s/^.* as /\t/p' dockerfile

requirements := justfile_directory() + '/requirements.txt'

django-shell:
    docker-compose run --rm web python manage.py shell

checkout-main:
    git checkout main

coverage:
    docker-compose run --rm web pytest --cov=. --cov-report=html
    open htmlcov/index.html

lint:
    docker-compose run --rm web black .

makemigrations:
    docker-compose run --rm web python manage.py makemigrations

migrate:
    docker-compose run --rm web python manage.py migrate

pull-main:
    git pull origin main

rebuild:
    docker-compose rm -f web
    docker-compose build --force-rm web

up:
    docker-compose up

shell:
    docker-compose run --rm web bash

test:
    docker-compose run --rm web pytest

tailwind:
	tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify

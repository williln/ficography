# ficography

A Django site for managing my fanfiction reading list. 

This project uses: 

- Python 3.10 
- Django 4.1

# Local Development 

Copy `env.template` to a local `.env` file 

    cp env.template .env 

# Management Commands 

## load_sample_fics 

Will generate a set of sample Fandom, Author, Character, Tag, and Ship objects, then use those objects to generate 100 Fic objects. 

_Does not necessarily add every Character in a Ship; it's expected that you do your own massaging of the data via the CLI or (coming soon) the Django admin if you need perfect sample data. 

    ./manage.py load_sample_fics

# Just Commands

I use [just](https://github.com/casey/just) to help standardize working with
this project. If you don't have it installed, for MacOS, run `brew install just`.

## just checkout-main
Runs `git checkout main`. 

## just coverage
Runs `pytest` generating an HTML coverage report and opens it in your local browser.

## just django-shell
Same as above but with `python manage.py shell` added, so you can start trying Django things more easily.

## just lint
Runs `black .` to format the codebase. 

## just {makemigrations or migrate}
Runs the corresponding [Django command](https://docs.djangoproject.com/en/3.0/topics/migrations/) in the `web` container.

## just pull-main
Runs `git pull origin main`.

## just rebuild
Removes the `web` container, then rebuilds `web`.
This should be used after each `just pip-compile`, as the project dependencies should have changed.

## just run
Runs `docker-compose up`

## just shell
Provides a bash prompt insided the `web` container. Useful for debugging and manual testing/investigation.

## just test
Runs `pytest` and `interrogate` in the `web` container.  Please: write, run, and document your tests.



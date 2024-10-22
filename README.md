# narvi-task

Recruitment task @ Narvi

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Usage
      $ docker compose -f docker-compose.local.yml build
      $ docker compose -f docker-compose.local.yml up

## Run tests
      $ docker compose -f docker-compose.local.yml run django pytest

## Test algorithm
Either run unit tests for group_names.py, use API at `GET /api/reset_folders` or bash into django container and run python file

## API endpoints

To test API:
1. Go to http://127.0.0.1:8000/api/docs (swagger)
2. Run `GET /api/reset_folders/` to populate folders/names (also resets after names moves)
3. Notice data with `GET /api/folders/`
4. Use `PATCH /api/names/{name}/move_name_into_folder` with `{"folder_name": "<destination_folder_name>"}` as request body to change name's folder
5. Use `POST /api/folders/` to create Folder

## Follow up questions
1. How do you productionize this application?
   As I was using cookiecutter there's already production ready docker containers setup with gunicorn and nginx. 
   For cloud deploy I'd use Terraform with Infrastracture as a Code repo to deploy with created images in CI/CD pipelines,
   but it's a rather simple infra as there's only postgresql database and django app.
2. How do you optimize it to work at a much bigger scale processing millions of words per second?
   If we expect millions of requests to create and move names into folders then I'd try to scale horizontally with Load Balancers and try not to lock out database.
   If we expect one big csv file with names then there's an issue with processing big file that could not fit in memory
   so we'd have to process file in chunks and try to adjust folders on the go rather than trying to find matching prefix in a file.
   Might also use Apache Kafka to do distributed stream processing

## TODO
add pre-commit with black, flake8, isort, mypy etc.


## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy narvi_task

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

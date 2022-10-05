# djangy
TLDR: Set up a [venv](https://docs.python.org/3/library/venv.html), activate it, then `pip install -r requirements.txt`  

This project also has an optional `pyproject.toml` file to install a `__pypackages__` cache via [PDM](https://github.com/pdm-project/pdm#what-is-pep-582), which implements [PEP-582](https://peps.python.org/pep-0582/) to manage dependencies.

It's pretty quick to set up with pipx:

```bash
# Install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# Install pdm via pipx
pipx install pdm
```

---

* migrate sqlite to postgres
* rotate secret keys in production

## making model changes

* Change your models (in models.py).
* Run python manage.py makemigrations to create migrations for those changes
* Run python manage.py migrate to apply those changes to the database

## create django project

```bash
pdm run django-admin startproject .
pdm run django-admin startproject djangy
```

## create, manage django app

```bash
# Create with startapp <name>
pdm run python3 manage.py startapp polls
pdm run python3 manage.py runserver

# Sync DB with models and migrations (apply schema changes to DB)
# https://docs.djangoproject.com/en/4.1/topics/migrations/#the-commands
pdm run python3 manage.py migrate
pdm run python3 manage.py sqlmigrate polls 0001
pdm run python3 manage.py check
```

## create superuser

`pdm run python3 manage.py createsuperuser`

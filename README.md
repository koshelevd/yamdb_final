![example workflow](https://github.com/koshelevd/yamdb_final/actions/workflows/main.yml/badge.svg)
# API "YamDB"

YamDB is project with DB of movies, books and songs reviews.

## Table of contents

- [Installing](#installing)
- [Build containers for project](#build-containers-for-project)
- [Collect static files](#collect-static-files)
- [Apply migrations](#apply-migrations)
- [Create superuser](#create-superuser)
- [Load initial data to database](#load-initial-data-to-database)

## Installing
You have to install [Docker Desktop](https://www.docker.com/) in order to run application.

## Build containers for project:
```
$ docker-compose up
```

## Collect static files
```
$ docker-compose run web python manage.py collectstatic
```

## Apply migrations
```
$ docker-compose run web python manage.py migrate
```

## Create superuser
```
$ docker-compose exec web python manage.py createsuperuser
```

## Load initial data to database
```
$ docker-compose run web python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
$ docker-compose run web python manage.py loaddata fixtures.json
```

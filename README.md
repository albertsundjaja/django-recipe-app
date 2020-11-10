# Django Recipe App

## to run test

```
docker-compose run app sh -c "python manage.py test && flake8"
```

## to add an app (module)

```
docker-compose run app sh -c "python manage.py startapp user"
```

### after creating new model

do model migrations

```
docker-compose run app sh -c "python manage.py makemigrations"
```

## to run the server

```
docker-compose up -d
```
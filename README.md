# Django Recipe App

## to run test

```
docker-compose run app sh -c "python manage.py test && flake8"
```

## to add an app (module)

```
docker-compose run app sh -c "python manage.py startapp user"
```

## to run the server

```
docker-compose up -d
```
# news_portal_02
Для создания проекта
```
django-admin startproject project
```

Для проведения первых миграций
```
python manage.py migrate
```

Для запуска
```
python manage.py runserver
```

Для начала нужно создать новое приложение
Добавить приложение в INSTALLED_APPS
Создать модели
Дальше промигрировать
```
python manage.py startapp name
python manage.py makemigrations
python manage.py migrate
```

Для запуска редиса и селери необходимо:
https://phoenixnap.com/kb/install-redis-on-mac

Terminal 1
```
redis-server
```

Terminal 2
```
celery -A newsportal worker -B -l info
```

Terminal 3
```
python manage.py runserver
```

```
docker run --name postgres -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=newsportal123 -e POSTGRES_DB=newsportal -e PGDATA=/var/lib/postgresql/data/pgdata -d -v "/Users/esconder/myprojects/newsportal/pgdata":/var/lib/postgresql/data  postgres:13.3
```
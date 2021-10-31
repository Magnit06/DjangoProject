#### Добавить в `/etc/hosts` строку `127.0.0.1 postgresdb` и `127.0.0.1 elasticsearch`

## Сборка и запуск докер-контейнеров
Из папки **samplesite** выполнить:
1. `docker-compose build`
2. `docker-compose up` (будете видеть логи) или `docker-compose up -d` (демонический процесс) - не будете видеть логи.
3. `python manage.py populate_db` наполняем БД тестовыми данными (процесс долгий, можно попить чай).

## Ссылка для входа в Адимн-панель
`http://127.0.0.1:8000/admin/`
1. login -> `admin`.
2. password -> `admin`.

## Для возможности тестирования
1. заходим в оболочку postgressql `docker exec -it postgressql bash`;
2. Подключаемся к БД `psql -U postgres`;
3. выполняем команду `ALTER USER djangouser CREATEDB;`.
Profit!


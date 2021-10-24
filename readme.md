Добавить в `/etc/hosts` строку `127.0.0.1 postgresdb` и `127.0.0.1 elasticsearch`

Ссылка для входа в Адимн-панель
`http://127.0.0.1:8000/admin/`

## Сборка и запуск докер-контейнеров
Из папки **samplesite** выполнить:
1. `docker-compose build`
2. `docker-compose up` (будете видеть логи) или `docker-compose up -d` (демонический процесс) - не будете видеть логи.


## Настраиваем супер пользователя
1. Из консоли `docker exec -it django-site bash`.
2. `python manage.py createsuperuser` - далее по указаниям из консоли.

## Для возможности тестирования
1. заходим в оболочку postgressql `docker exec -it postgressql bash`;
2. Подключаемся к БД `psql -U postgres`;
3. выполняем команду `ALTER USER djangouser CREATEDB;`.
Profit!


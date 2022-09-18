# Сервис переноса данных

## Очистка БД

- Сначала получаем список контейнеров
```bash
docker ps
```

- Из которого копируем container_id

- И вставляем container_id в запрос:
```bash
docker exec -it container_id python -m sqlite_to_postgres.clear_db
```



# ShareCare Backend

Приложение для управления медицинскими данными пациентов с удалённым доступом.

## Требования

- Docker
- Python 3.13+

## Сборка Docker-образа

```bash
docker build -t grafov1/backend:v1 .
```

## Запуск контейнера

```bash
docker run -p 8000:8000 grafov1/backend:v1
```

Приложение будет доступно на `http://localhost:8000`

## Docker Hub

Образ выложен в Docker Hub: `grafov1/backend:v1`
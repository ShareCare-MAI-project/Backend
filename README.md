# QuickStart (Настройка проекта)
1) Скачать uv [\*тык*](https://docs.astral.sh/uv/getting-started/installation/)
2) Прописать `uv sync`
3) Запуск `uv run -m app.main`
> [!IMPORTANT]
> Лучше запускать всё-таки в докере:
> - Засетапленная БД
> - Удобная настройка окружения
> - Авто-перезапуск 

# QuickStart (Docker)
1) Скачать docker и docker-compose [\*тык*](https://docs.docker.com/compose/install/)
2) Настроить переменные окружения
    - скопировать .env.sample в .env
    - заполнить .env (незаполненные данные без комментариев могут быть любыми)
3) _Сбилдить_ сервер `docker-compose build` (необходимо прописывать каждый раз, когда меняем зависимости)
4) Запустить контейнер `docker-compose up` (в первый раз он будет скачивать postgres)
5) Вы великолепны

## Кое-что ещё про докер
- Доступ снаружи: 
  - Всё зависит от переменных .env (SERVER_PORT и POSTGRES_PORT) # Приведу пример с 8080 и 7432 
  - К серверу: `localhost:8080` или `0.0.0.0:8080`
  - Аналогично с бд, но другой порт =)
- Прочитать [README.md в папке db](./db/README.md)
- Контейнеры можно запустить в фоне `docker compose up -d` (ввод с клавиатуры останется)
- Если запустить контейнеры в фоне, то в них можно запускать другие процессы
   - `docker compose exec -it app sh` – запустить bash на минималках в контейнере с питоном
   - `docker compose exec -it postgres sh` – то же самое, но для контейнера с бд
   - `exit` – выход


# Техническая информация
### Стек:
- FastApi
- SQLAlchemy
- Pydantic
- PostgreSQL
- Docker (compose)

### Модули:
- **Auth**: Авторизация, регистрация пользователей, работа с OTP (OneTimePassword)
- **Core**: Общий конфиг и настройка БД
- **Items** и **Requests**: Предметы и запросы (Models, CRUD, Schemas, Mappers) 
- **ShareCare** и **FindHelp**: Фича-модули из мобилки (Специальные роуты под мобилку и т.п.)
- **Utils**: Инициализация сервера, Dependencies, Декораторы
- [**ML**](https://github.com/ShareCare-MAI-project/Backend/tree/fixing/ml-module): Пока не смёржен

>WIP: Расписать про дб

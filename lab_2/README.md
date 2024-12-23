# Telegram-bot с моделью Mistral и RAG сервисом

## Описание docker-compose.yml

Наш `docker-compose.yml` файл определяет следующие сервисы:

1. **init**: Сервис инициализации, использующий образ busybox.

   - Выполняет простую команду для обозначения завершения инициализации.
2. **app**: Основное приложение (Telegram бот).

   - Собирается из Dockerfile в текущем контексте.
   - Зависит от сервисов `db` и `faiss`.
   - Использует volume для логов.
   - Прокидывает порт 8080.
   - Использует переменные окружения из .env файла.
   - Имеет настройки healthcheck.
3. **faiss**: Сервис для FAISS (Fast Algorithm for Similarity Search).

   - Использует предопределенный образ faiss.
   - Использует volume для хранения данных.

Все сервисы подключены к одной сети `bot_network`.

## Вопросы и ответы

### 1. Можно ли ограничивать ресурсы для сервисов в docker-compose.yml?

Да, в Docker Compose можно ограничивать ресурсы для сервисов. Это делается с помощью настроек в секции `deploy` для каждого сервиса. Например:

```yaml
services:
  myapp:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
```

Это ограничит использование CPU до 50% одного ядра и память до 512 мегабайт.
Важно отметить, что для использования этих настроек нужно запускать Docker Compose в режиме swarm: docker-compose --compatibility up.Это ограничит использование CPU до 50% одного ядра и память до 512 мегабайт.
Важно отметить, что для использования этих настроек нужно запускать Docker Compose в режиме swarm: docker-compose --compatibility up.

### 2. Как можно запустить только определенный сервис из docker-compose.yml, не запуская остальные?

Чтобы запустить только определенный сервис из docker-compose.yml, не запуская остальные, можно использовать команду:

```
docker-compose up <имя_сервиса>
```

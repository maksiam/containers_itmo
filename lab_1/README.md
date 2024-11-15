# Телеграм-бот с Mistral AI

## Плохие практики в Dockerfile

1. Использование latest тега (`FROM ubuntu:latest`):
   - Почему плохо: Непредсказуемость версии базового образа.
   - Исправление: Используем конкретную версию Python (`FROM python:3.9-slim`).

2. Установка лишних пакетов:
   - Почему плохо: Увеличивает размер образа и поверхность атаки.
   - Исправление: Используем легковесный образ python:3.9-slim.

3. Копирование всех файлов (`COPY . /app`):
   - Почему плохо: Может включать ненужные файлы, увеличивая размер образа.
   - Исправление: Копируем только необходимые файлы.

4. Хранение секретов в Dockerfile:
   - Почему плохо: Небезопасно хранить секреты в образе.
   - Исправление: Используем переменные окружения или secrets management.

5. Запуск от root:
   - Почему плохо: Небезопасно, предоставляет излишние привилегии.
   - Исправление: Создаем и используем непривилегированного пользователя.

## Плохие практики контейнеризации

### Запуск с root-привилегиями
Использование контейнеров с root-правами увеличивает риск безопасности. Если контейнер будет скомпрометирован, атакующий получит полный доступ к хост-системе.

### Игнорирование ограничений ресурсов
Отсутствие лимитов на использование CPU и памяти может привести к тому, что один контейнер исчерпает ресурсы хоста, влияя на работу других контейнеров и самой системы.

### Использование устаревших образов
Применение старых версий образов или отсутствие регулярных обновлений увеличивает риск наличия известных уязвимостей в вашей системе.

### Хранение секретов в образах
Включение паролей, ключей API и других чувствительных данных непосредственно в образ контейнера делает эту информацию доступной для всех, кто имеет доступ к образу.

### Игнорирование принципа неизменяемости
Внесение изменений в работающие контейнеры вместо пересоздания их из обновленных образов усложняет отслеживание изменений и может привести к расхождениям между средами.

### Запуск нескольких процессов в одном контейнере
Объединение нескольких сервисов в одном контейнере усложняет масштабирование, мониторинг и обновление отдельных компонентов системы.

## Запуск контейнеров

Для запуска "плохого" контейнера:

```bash
docker build -t bad-bot -f Dockerfile.bad .
docker run -d --name bad-bot-container bad-bot
```

```bash
docker build -t good-bot -f Dockerfile.good .
docker run -d --name good-bot-container -v /path/on/host:/app/logs -e TELEGRAM_BOT_TOKEN=your_token -e MISTRAL_API_KEY=your_key good-bot
```
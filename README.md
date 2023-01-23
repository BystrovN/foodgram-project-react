
![foodgram CI/CD](https://github.com/BystrovN/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

# Welcome!

Проект **Foodgram** - «Продуктовый помощник».
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Документация

Подробный перечень запросов, параметров, необходимых прав доступа и примеров ответов находится в документации и расположен по адресу - **localhost/redoc/**

## Установка
Все команды терминала в данном разделе выполняются с правами суперпользователя. 

1. Для запуска проекта необходимо заполнить файл **.env** с переменными окружения. Важно, чтобы указанный файл находился в одной директории с **docker-compose.yaml**. Пример заполнения: 
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

2. Для развертывания приложения необходимо из директории *infra/* выполнить команду. Сбор статики и миграции БД применяются автоматически в онце сборки контейнера.
```
	docker-compose up -d
```
	Флаг -d выполнит развертывание в фоновом режиме, что позволит осуществлять управление контейнерами из этого же окна терминала.

3. Создадим суперпользователя:
```
	docker-compose exec web python manage.py createsuperuser
```

4. Для ознакомления с возможностями сервиса в корневой директории  присутствует дамп заполненной базы данных - файл **fixtures.json**.  Для выгрузки применяется команда:
```
	docker-compose exec web python manage.py loaddata fixtures.json
```

## Технологии

 - Python - 3.11.1
 - Django - 4.1.4
 - Django Rest Framework - 3.14.0
 - Postgres - 15.1
 - Gunicorn - 20.1.0
 - Nginx - 1.21.3
 - Docker
 - Docker Compose


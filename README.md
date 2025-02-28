# Проект Foodgram

Дипломный проект курса «Python-разработчик» от компании Яндекс Практикум.

## Описание проекта:

Foodgram - сайт, на котором пользователи публикуют свои рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Зарегистрированным пользователям также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Сайт доступен по даресу: [oritum.zapto.org](oritum.zapto.org)

## Авторы и разработчики:

* *Яндекс Практикум (автор проекта):*  [Сайт](https://practicum.yandex.ru/)
* *Олег Ритум (backend developer):* [Github](https://github.com/oritum)

  Год разработки: *2025.*

## Стек технологий:

* Python 3.9
* Django 3.2
* Django Rest Framework 3.12.4

## В проекте реализована автоматизация процессов непрерывной интеграции (CI) и непрерывной доставки (CD) с использованием [GitHub Actions](https://github.com/features/actions)

## Развертывание проекта на локальном компьютере:

#### Шаг 1: Клонирование репозитория

```shell
 clone git@github.com:<username>/foodgram.git
```

```shell
cd foodgram/backend
```

#### Шаг 2: Создание и активация виртуального окружения

```shell
python -m venv venv
```

```shell
source venv/bin/activate
```

#### Шаг 3: Установка зависимостей

```shell
python -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

#### Шаг 4: Применение миграций

```shell
python manage.py migrate
```

#### Шаг 5: Создание файла с переменными окружения `.env`

```shell
touch .env
```

###### Требуемые переменные:

```shell
ENV=
SECRET_KEY=
SHORTLINK_SALT=
ALLOWED_HOSTS=
DB_PORT=
DB_HOST=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

#### Шаг 6: Импорт справочника ингридиентов из csv-файлов в базу данных

```shell
python manage.py import_data_from_csv
```

#### Шаг 7: Запуск сервера разработки

```shell
python manage.py runserver
```

## Развертывание проекта на удалённом сервере

#### Шаг 1: Копирование файла `docker-compose.production.yml` на сервер в директорию с приложением:

```shell
scp /путь/к/локальному/файлу username@server_ip:/путь/к/удаленной/папке
```

#### Шаг 2: Создание в директории приложения файла с переменными окружения `.env`:

```shell
sudo nano .env

ENV=
SECRET_KEY=
SHORTLINK_SALT=
ALLOWED_HOSTS=
DB_PORT=
DB_HOST=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

#### Шаг 3: Установка на сервере `docker` и `docker compose`:

```shell
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
```

#### Шаг 4: Сборка контейнеров проекта:

```shell
sudo docker compose -f docker-compose.production.yml up -d
```

#### Шаг 5: Применение миграций, сбор статики и копирование статики, импорт справочника ингридиентов:

```shell
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_data_from_csv
```

#### *После этих шагов проект будет доступен локально по адресу `127.0.0.1:8000`*

#### Шаг 6: Настройка веб-сервера для доступа переадресации запросов к контейнеру `gateway`

## Примеры некоторых запросов и ответов к API:

### Регистрация нового пользователя

**Запрос:**

```json
POST .../api/users/

{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Иванов",
  "password": "Qwerty123"
}
```

**Ответ:**

```json
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Иванов"
}
```

### Получение токена

**Запрос:**

```json
POST .../api/auth/token/login/

{
  "password": "string",
  "email": "string"
}
```

**Ответ:**

```json
{
  "auth_token": "string"
}
```

### Добавление аватара

**Запрос:**

```json
PUT .../api/users/me/avatar

{
  "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
}
```

**Ответ:**

```json
{
  "avatar": "http://foodgram.example.org/media/users/image.png"
}
```

### Создание рецепта

**Запрос:**

```json
POST .../api/recipes/

{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

**Ответ:**

```json
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Иванов",
    "is_subscribed": false,
    "avatar": "http://foodgram.example.org/media/users/image.png"
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.png",
  "text": "string",
  "cooking_time": 1
}
```

### Получение списка рецептов

**Запрос:**

```json
GET .../api/recipes/
```

**Ответ:**

```json
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Иванов",
        "is_subscribed": false,
        "avatar": "http://foodgram.example.org/media/users/image.png"
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.png",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

### Добавление рецепта в список покупок

**Запрос:**

```json
POST .../api/recipes/{id}/shopping_cart/
```

**Ответ:**

```json
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.png",
  "cooking_time": 1
}
```

### Подписка на пользователя

**Запрос:**

```json
POST .../api/users/{id}/subscribe/
```

**Ответ:**

```json
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Иванов",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.png",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0,
  "avatar": "http://foodgram.example.org/media/users/image.png"
}
```

### Получение списка ингридиентов

**Запрос:**

```json
GET .../api/ingredients/
```

**Ответ:**

```json
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```

### Получение списка тегов

**Запрос:**

```json
GET .../api/tags/
```

**Ответ:**

```json
[
  {
    "id": 0,
    "name": "Завтрак",
    "slug": "breakfast"
  }
]
```

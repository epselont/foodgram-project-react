![Foodgram Status](https://github.com/epselont/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Проект Foodgram - «Продуктовый помощник»
Сервис, который позволяет пользователям публиковать свои рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Сайт

http://epselont.ddns.net/
Логин: review@review.re
Пароль: Review@123

## Используемые технологии:

<img title="Python" alt="Python" width="40px" 
  src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" />&nbsp;
<img title="Django" alt="Django" width="40px"
  src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain.svg" />&nbsp;
<img title="DjangoRestFramework" alt="DjangoRest" width="40px"
  src="https://s3.amazonaws.com/media-p.slid.es/uploads/708405/images/4005243/django_rest_500x500.png" />&nbsp;
<img title="Gunicorn" alt="Gunicorn" width="40px"
  src="https://github.com/epselont/epselont/blob/main/icons/gunicorn.png" />&nbsp;
<img title="PostgreSQL" alt="PostgreSQL" width="40px"
  src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-plain-wordmark.svg" />&nbsp;
<img title="Docker" alt="Docker" width="40px"
  src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" />&nbsp;
<img title="NGINX" alt="NGINX" width="45px"
  src="https://github.com/devicons/devicon/blob/master/icons/nginx/nginx-original.svg" />&nbsp;


## Запуск проекта через Docker

Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

Клонируйте репозиторий с проектом на свой компьютер.
В терминале из рабочей директории выполните команду:
```
git clone https://github.com/epselont/foodgram-project-react.git
```
Перейдите в папку foodgram-project-react/infra
```
cd foodgram-project-react/infra
```

Выполните команду:
```
docker compose up -d --build
```

### Выполните миграции:
```
docker compose exec backend python manage.py migrate
```

### Загрузите статику:
```
docker compose exec backend python manage.py collectstatic --no-input
```

### Заполните базу тестовыми данными:
```
docker compose exec web python manage.py load_ingredients
```
Теперь приложение будет доступно в браузере по адресу localhost/admin/

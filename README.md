# test_for_Rishat
Тестовое задание для компании 'Ришат'

Текст задания находится в файле task.txt

## Как запустить проект:
Клонировать репозиторий на свой компьютер
https://github.com/filimonka/test_for_Rishat

Перейти в папку stripe_project:
```cd stripe_project/```

Создать .env файл, с параметрами:
``` 
    STRIPE_PUBLIC_KEY=<your_stripe_public_key>
    STRIPE_SECRET_KEY=<your_stripe_secret_key>
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=<your postgres_username>
    POSTGRES_PASSWORD=<your postgres_password>
    DB_HOST=db
    DB_PORT=5432
```
Запустить docker-compose:

```docker-compose up -d```

Выполнить миграции:

```docker-compose exec web python manage.py migrate```

Собрать staticfiles:

```docker-compose exec web python manage.py collectstatic --no-input```

Создать пользователя с правами администратора:

```docker-compose exec web python manage.py createsuperuser```

Перейдите на страницу http://localhost/admin/ для доступа к админ-зоне проекта,
создайте несколько объектов товаров и, при желании, заказов, а также Discounts.
Пожалуйста, не добавляйте в один заказ товары с ценой в разной валюте, я пока не решила эту проблему. 
Пока думаю в сторону валидации модели OrderAdmin, для запрета этого действия. 

Перейдите на страницу http://localhost/item/<int:id>/, действуйте!

http://localhost/check_order/<int:id>/ аналогична предыдущей, но для оплаты заказа.

4242 4242 4242 4242 - тестовые данные номера карты для успешного платежа

4000 0025 0000 3155 - тестовые данные номера карты для ответа о необходимости аутентификации

4000 0000 0000 9995 - этот платеж будет отклонен

API Эндпойнты 
http://localhost/buy/<int:id>/ 

http://localhost/pay_for_order/<int:id>/ 

возвращают id платежной сессии.

_Tech_stack:_
__Django, Stripe, Docker__


_Author:_
__Kate https://github.com/filimonka__

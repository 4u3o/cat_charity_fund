Generic single-database configuration with an async dbapi.  
alembic==1.7.7

Для работы автогенерации миграций импортируйте все модели в *app/core/base.py*.


Посмотреть историю миграций:

    alembic history --verbose

Сгенерировать новую миграцию:

    alembic revision --autogenerate -m 'name'

Применить миграции:

    alembic upgrade head

Отменить последнюю миграцию:

    alembic downgrade -1

Отменить все миграции:

    alembic downgrade base


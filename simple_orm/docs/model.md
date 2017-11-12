## Построение модели данных

Для описания модели необходимо объявить класс унасследованный от класса BaseTable.

Название таблицы задаётся атрибутом класса _ _ table_name _ _ .

Поля таблицы задаются с помощью классов-полей: IntegerField, BooleanField, TextField

## Параметры инициализации классов-полей :
* not_null: является ли поле not null
* primary_key: является ли поле первичным ключом
* foreign_key: ссылка на внешний ключ (инстанс класс-поля)
* default_value: значение по умолчанию

## Пример:

    from simple_orm.table import BaseTable
    from simple_orm.fields import IntegerField, BooleanField, TextField
    from simple_orm.session import Session


    class City(BaseTable):
        __table_name__ = 'city'
    
        id = IntegerField(primary_key=True)
        name = TextField(not_null=True)


    class User(BaseTable):
        __table_name__ = 'users'
    
        id = IntegerField(primary_key=True)
        name = TextField(not_null=True)
        id_city = IntegerField(foreign_key=City.id)
        active = BooleanField(not_null=True, default_value=1)
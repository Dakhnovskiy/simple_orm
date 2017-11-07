# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

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


session = Session(None)

print(session.query(City, User).create())
print(session.query(User).drop())

print(session.query(User, City.name).select().filter(
        User.name == City.name,
        User.name <= 'asd',
        logical_opertor_inner='OR'
    ).filter(
        City.name == 'друг'
    )
)

print(session.query(User).delete().filter(User.name == 'Вася'))

user = User(id=1, name='Вася')
print(session.query().insert(user))
print(session.query(User).update(name='Петя').filter(User.id == 1))
# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from simple_orm.table import BaseTable
from simple_orm.fields import IntegerField, BooleanField, TextField
from simple_orm.session import Session


class User(BaseTable):
    __table_name__ = 'users'

    id = IntegerField(primary_key=True)
    name = TextField(not_null=True)
    active = BooleanField(not_null=True, default_value=1)


class Relation(BaseTable):
    __table_name__ = 'relations'

    id = IntegerField(primary_key=True)
    name = TextField(not_null=True)


session = Session(None)

print(session.create(User, Relation))
print(session.drop(User))

print(session.select(User, Relation.name).filter(
        User.name == Relation.name,
        User.name <= 'asd',
        logical_opertor_inner='OR'
    ).filter(
        Relation.name == 'друг'
    )
)

print(session.delete(User).filter(User.name == 'Вася'))

user = User(id=1, name='Вася')
print(session.insert(user))

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

print(session.get_create_table_script(User))
print(session.get_drop_table_script(User))

print(session.select(User, Relation.name))
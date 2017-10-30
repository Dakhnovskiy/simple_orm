# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from simple_orm.table.base_table import BaseTable
from simple_orm.fields import IntegerField, BooleanField, TextField


class User(BaseTable):
    __table_name__ = 'users'

    id = IntegerField(primary_key=True)
    name = TextField(not_null=True)
    active = BooleanField(not_null=True, default_value=1)

print(User.get_create_table_script())
print(User.get_drop_table_script())
print(User.get_select_script())
print(User.get_select_script(User.id, User.name))

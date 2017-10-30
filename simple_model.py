# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from simple_orm.table.base_table import BaseTable
from simple_orm.fields import IntegerField, BooleanField, TextField


class User(BaseTable):
    __table_name__ = 'users'

    id = IntegerField(primary_key=True)

User.get_fields()

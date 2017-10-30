# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from ..fields import BaseField


class BaseTable:

    __table_name__ = None

    __create_table_template = 'CREATE TABLE {table_name} (\n{columns_defenition}\n)'
    __drop_table_template = 'DROP TABLE {table_name}'

    @classmethod
    def get_create_table_script(cls):
        columns_defenition = ',\n'.join((field[0] + ' ' + field[1].defenition for field in cls.get_fields()))

        return cls.__create_table_template.format(
            table_name=cls.__table_name__,
            columns_defenition=columns_defenition
        )
    
    @classmethod
    def get_drop_table_script(cls):
        return cls.__drop_table_template.format(table_name=cls.__table_name__)

    def get_insert_script(self):
        pass

    def get_update_script(self):
        pass

    @classmethod
    def get_fields(cls):
        return [(attr, getattr(cls, attr)) for attr in cls.__dict__ if isinstance(getattr(cls, attr), BaseField)]

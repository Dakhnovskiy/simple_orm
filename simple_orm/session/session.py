# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from .query import Query
from ..fields import BaseField
from ..table import BaseTable


class Session:
    
    def __init__(self, connect):
        self.__connect = connect
        super().__init__()
    
    __create_table_template = 'CREATE TABLE {table_name} (\n{columns_defenition}\n)'
    __drop_table_template = 'DROP TABLE {table_name}'
    __select_template = 'SELECT {columns_names} FROM {table_name}'
    __insert_template = 'INSERT INTO {table_name}({columns_names})\nVALUES ({VALUES})'
    __update_template = 'UPDATE {table_name} SET\n{columns_values}'
    __delete_template = 'DELETE FROM {table_name}'

    def get_create_table_script(self, cls):
        columns_defenition = ',\n'.join((field[0] + ' ' + field[1].defenition for field in cls.get_fields()))

        return self.__create_table_template.format(
            table_name=cls.__table_name__,
            columns_defenition=columns_defenition
        )

    def get_drop_table_script(self, cls):
        return self.__drop_table_template.format(table_name=cls.__table_name__)

    def __get_select_script(self, columns_names, table_name):
        return self.__select_template.format(columns_names=', '.join(columns_names), table_name=table_name)

    def get_delete_script(self):
        pass

    def get_insert_script(self):
        pass

    def get_update_script(self):
        pass

    def select(self, *args):
        columns = []

        # получить список колонок из args
        for arg in args:
            if isinstance(arg, BaseField):
                columns.append(arg)
            elif issubclass(arg, BaseTable):
                columns.extend([field[1] for field in arg.get_fields()])
            else:
                # TODO raise
                pass

        table_name = columns[0].table_name
        columns_names = [col.table_name + '.' + col.name for col in columns]

        return Query(self.__get_select_script(columns_names, table_name))

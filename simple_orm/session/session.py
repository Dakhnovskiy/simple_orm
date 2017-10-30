# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


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

    def get_select_script(self, cls, *fields):
        columns_names = [field[0] for field in cls.filter_fields(*fields)]
        return self.__select_template.format(columns_names=', '.join(columns_names), table_name=cls.__table_name__)

    def get_delete_script(self):
        pass

    def get_insert_script(self):
        pass

    def get_update_script(self):
        pass

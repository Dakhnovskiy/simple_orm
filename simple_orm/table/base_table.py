# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from ..fields import BaseField


class BaseTable:

    __table_name__ = None

    __create_table_template = 'CREATE TABLE {table_name} (\n{columns_defenition}\n)'
    __drop_table_template = 'DROP TABLE {table_name}'
    __select_template = 'SELECT {columns_names} FROM {table_name}'
    __insert_template = 'INSERT INTO {table_name}({columns_names})\nVALUES ({VALUES})'
    __update_template = 'UPDATE {table_name} SET\n{columns_values}'
    __delete_template = 'DELETE FROM {table_name}'

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

    @classmethod
    def get_select_script(cls, *fields):
        columns_names = [field[0] for field in cls.filter_fields(*fields)]
        return cls.__select_template.format(columns_names=', '.join(columns_names), table_name=cls.__table_name__)

    @classmethod
    def get_delete_script(cls):
        pass

    @classmethod
    def get_insert_script(cls):
        pass

    @classmethod
    def get_update_script(cls):
        pass

    @classmethod
    def get_fields(cls):
        """
        возвращает набор полей таблицы
        :return: список пар [(название колонки, инстанс колонки),..]
        """
        return [(attr, getattr(cls, attr)) for attr in cls.__dict__ if isinstance(getattr(cls, attr), BaseField)]

    @classmethod
    def filter_fields(cls, *fields):
        """
        Возвращает набор полей таблицы, оставляя только поля из переданных в fields
        :comment: Если fields не переданы, то возвращает весь набор полей таблицы
        :param fields: Инстансы полей
        :return: список пар [(название колонки, инстанс колонки),..]
        """
        return filter(lambda field: field[1] in fields or not fields, cls.get_fields())

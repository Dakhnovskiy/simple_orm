# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from ..fields import BaseField
from ..table import BaseTable


class Query:

    __create_table_template = 'CREATE TABLE {table_name} (\n{columns_defenition}\n);'
    __drop_table_template = 'DROP TABLE {table_name};'
    __select_template = 'SELECT {columns_names} FROM {table_name}'
    __insert_template = 'INSERT INTO {table_name}({columns_names})\nVALUES ({values})'
    __update_template = 'UPDATE {table_name} SET\n{columns_values}'
    __delete_template = 'DELETE FROM {table_name}'

    @property
    def query_str(self):
        query = self.__query_str
        if self.__filter_str:
            query += '\nWHERE ' + self.__filter_str
        return query

    def __init__(self, *args, query_str=None):
        super().__init__()

        if query_str is None:
            query_str = ''
        self.__query_str = query_str
        self.__filter_str = ''

        self.__tables = set()
        self.__fields = []
        self.__main_table = None

        for arg in args:
            if isinstance(arg, BaseField):
                self.__fields.append(arg)
                self.__set_main_table(arg.table_class)
            elif issubclass(arg, BaseTable):
                self.__tables.add(arg)
                self.__set_main_table(arg)
            else:
                # TODO raise
                pass

    def __set_main_table(self, table):
        if self.__main_table is None:
            self.__main_table = table

    def __str__(self):
        return self.query_str

    def __get_create_table_script(self, cls):
        columns_defenition = ',\n'.join((field[0] + ' ' + field[1].defenition for field in cls.get_fields()))

        return self.__create_table_template.format(
            table_name=cls.__table_name__,
            columns_defenition=columns_defenition
        )

    def __get_drop_table_script(self, cls):
        return self.__drop_table_template.format(table_name=cls.__table_name__)

    def __get_select_script(self, table_name, columns_names):
        return self.__select_template.format(columns_names=', '.join(columns_names), table_name=table_name)

    def __get_delete_script(self, table_name):
        return self.__delete_template.format(table_name=table_name)

    def __get_insert_script(self, table_name, column_value_map):
        return self.__insert_template.format(
            table_name=table_name,
            columns_names=', '.join(column_value_map.keys()),
            values=', '.join(map(str, column_value_map.values()))
        )

    def __get_update_script(self, table_name, columns_values):
        return self.__update_template.format(
            table_name=table_name,
            columns_values=',\n'.join(['%s = %s' % (column, value) for column, value in columns_values.items()])
        )

    def __set_query_str(self, query):
        self.__query_str = query

    def create(self):
        """
        Создать Query со скриптами создания таблиц
        :return: инстанс Query
        """
        self.__set_query_str('\n'.join(map(self.__get_create_table_script, self.__tables)))
        return self

    def drop(self):
        """
        Создать Query со скриптами удаления таблиц
        :return: инстанс Query
        """
        self.__set_query_str('\n'.join(map(self.__get_drop_table_script, self.__tables)))
        return self

    def select(self):
        """
        Создать Query со скриптом select
        :return: инстанс Query
        """

        # получить список колонок из self.__tables и self.__fields
        columns = self.__fields[:]

        for table in self.__tables:
            columns.extend([field[1] for field in table.get_fields()])

        columns_names = [col.full_name for col in columns]

        self.__set_query_str(self.__get_select_script(self.__main_table.__table_name__, columns_names))
        return self

    def delete(self):
        """
        Создать Query со скриптом delete
        :return: инстанс Query
        """
        self.__set_query_str(self.__get_delete_script(table_name=self.__main_table.__table_name__))
        return self

    def insert(self, table_record):
        """
        Создать Query со скриптом insert
        :param: table_record: инстанс таблицы
        :return: инстанс Query
        """
        self.__set_query_str(self.__get_insert_script(
            table_name=table_record.__class__.__table_name__,
            column_value_map=table_record.column_value_map
        ))
        return self

    def update(self, **kwargs):
        """
        Создать Query со скриптом update
        :param: kwargs: поля таблицы для обновления
        :return: инстанс Query
        """

        columns_values = {
            field_name: self.__main_table.get_field_by_name(field_name).__class__.quoted_value(value)
            for field_name, value in kwargs.items()
        }

        self.__set_query_str(self.__get_update_script(
            table_name=self.__main_table.__table_name__,
            columns_values=columns_values
        ))
        return self

    def filter(self, *condition_expressions, logical_opertor_inner=None, logical_opertor_outer=None):
        """
        Добавляет условие ограничения
        :param: condition_expressions: условие ограничения (Table.column == 10, Table.column == Table2.column2)
        :param: logical_opertor_inner: логический оператор для внутреннего соединения переданных условий
        :param: logical_opertor_outer: логический оператор для внешнего соединения переданных условий
        :return: экземляр Query
        """
        if logical_opertor_inner is None:
            logical_opertor_inner = 'AND'
        if logical_opertor_outer is None:
            logical_opertor_outer = 'AND'

        assert logical_opertor_inner.upper() in ('AND', 'OR'), 'logical_opertor_inner choice of OR, AND'
        assert logical_opertor_outer.upper() in ('AND', 'OR'), 'logical_opertor_outer choice of OR, AND'

        filter_condition = '(%s)' % ((' %s ' % logical_opertor_inner).join(condition_expressions))
        self.__filter_str += (' %s ' % logical_opertor_outer if self.__filter_str else '') + filter_condition

        return self

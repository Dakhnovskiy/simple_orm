# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from ..fields import BaseField
from ..table import BaseTable


class Query:

    __create_table_template = 'CREATE TABLE {table_name} (\n{columns_defenition}\n{foreign_keys_defenition}\n)'
    __drop_table_template = 'DROP TABLE {table_name}'
    __select_template = 'SELECT {columns_names} FROM {table_name}'
    __insert_template = 'INSERT INTO {table_name}({columns_names})\nVALUES ({values})'
    __update_template = 'UPDATE {table_name} SET\n{columns_values}'
    __delete_template = 'DELETE FROM {table_name}'

    @property
    def query_str(self):
        query = self.__query_str
        if self.__join_str:
            query += self.__join_str
        if self.__filter_str:
            query += '\nWHERE ' + self.__filter_str
        return query

    @property
    def query_list(self):
        query_list = self.__query_list[:]
        if not query_list:
            query_list.append(self.query_str)

        return query_list

    def __init__(self, *args, query_str=None, connect=None):
        super().__init__()

        self.__connect = connect
        if query_str is None:
            query_str = ''
        self.__query_str = query_str
        self.__filter_str = ''
        self.__join_str = ''

        self.__query_list = []

        self.__tables = set()
        self.__fields = []
        self.__main_table = None

        for arg in args:
            if isinstance(arg, BaseField):
                self.__fields.append(arg)
            elif issubclass(arg, BaseTable):
                self.__tables.add(arg)
                self.__fields.extend([field[1] for field in arg.get_fields()])
            else:
                # TODO raise
                pass
        if self.__fields:
            self.__main_table = self.__fields[0].table_class

    def __str__(self):
        return str(self.query_list)

    def __get_create_table_script(self, cls):
        fields = cls.get_fields()
        columns_defenition = ',\n'.join((field[0] + ' ' + field[1].defenition for field in fields))
        foreign_keys_defenition = '\n'.join(
            ', ' + field[1].foreign_key_defenition for field in fields if field[1].foreign_key_defenition
        )

        return self.__create_table_template.format(
            table_name=cls.__table_name__,
            columns_defenition=columns_defenition,
            foreign_keys_defenition=foreign_keys_defenition
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

    def __add_filter_str(self, filter_str, logical_opertor):
        self.__filter_str += (' %s ' % logical_opertor if self.__filter_str else '') + filter_str

    def __add_join_str(self, join_str):
        self.__join_str += join_str

    def __clear_query_str(self):
        self.__query_str = ''
        self.__join_str = ''
        self.__filter_str = ''

    def __clear_query_list(self):
        self.__query_list.clear()

    def __add_to_query_list(self, query_str):
        self.__query_list.append(query_str)

    def clear(self):
        """
        Очистить запросы
        """
        self.__clear_query_list()
        self.__clear_query_str()

    def create(self):
        """
        Создать Query со скриптами создания таблиц
        :return: инстанс Query
        """
        for table in self.__tables:
            self.__add_to_query_list(self.__get_create_table_script(table))
        return self

    def drop(self):
        """
        Создать Query со скриптами удаления таблиц
        :return: инстанс Query
        """
        for table in self.__tables:
            self.__add_to_query_list(self.__get_drop_table_script(table))
        return self

    def select(self):
        """
        Создать Query со скриптом select
        :return: инстанс Query
        """

        columns_names = [col.full_name for col in self.__fields]

        self.__set_query_str(self.__get_select_script(self.__main_table.__table_name__, columns_names))
        return self

    def delete(self):
        """
        Создать Query со скриптом delete
        :return: инстанс Query
        """
        self.__set_query_str(self.__get_delete_script(table_name=self.__main_table.__table_name__))
        return self

    def insert(self, *table_records):
        """
        Создать Query со скриптом insert
        :param table_records: инстансы классов-таблиц
        :return: инстанс Query
        """
        for table_record in table_records:
            self.__add_to_query_list(self.__get_insert_script(
                table_name=table_record.__class__.__table_name__,
                column_value_map=table_record.column_value_map
            ))
        return self

    def update(self, **kwargs):
        """
        Создать Query со скриптом update
        :param kwargs: поля таблицы для обновления
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
        :param condition_expressions: условие ограничения (Table.column == 10, Table.column == Table2.column2)
        :param logical_opertor_inner: логический оператор для внутреннего соединения переданных условий
        :param logical_opertor_outer: логический оператор для внешнего соединения переданных условий
        :return: инстанс Query
        """
        if logical_opertor_inner is None:
            logical_opertor_inner = 'AND'
        if logical_opertor_outer is None:
            logical_opertor_outer = 'AND'

        assert logical_opertor_inner.upper() in ('AND', 'OR'), 'logical_opertor_inner choice of OR, AND'
        assert logical_opertor_outer.upper() in ('AND', 'OR'), 'logical_opertor_outer choice of OR, AND'

        filter_condition = '(%s)' % ((' %s ' % logical_opertor_inner).join(condition_expressions))
        self.__add_filter_str(filter_condition, logical_opertor_outer)

        return self

    def join(self, table, auto_join=True):
        """
        Добавляет join таблицы к запросу
        :param table: класс-таблица
        :param auto_join: флаг(генерировать условие присеодинения для таблиц с FK, если True)
        :return: инстанс Query
        """
        join_str = '\nJOIN %s' % table.__table_name__
        if auto_join:
            field_foreign_key = self.__main_table.get_foreign_field_by_table(table) or \
                                table.get_foreign_field_by_table(self.__main_table)
            if field_foreign_key:
                join_str += ' ON %s = %s' % (field_foreign_key.full_name, field_foreign_key.foreign_key.full_name)

        self.__add_join_str(join_str)
        return self

    def execute(self):
        """
        Выполняет запросы, собранные в инстансе Query
        :return: курсор
        """
        cur = self.__connect.cursor()
        for query in self.query_list:
            cur.execute(query)
        return cur

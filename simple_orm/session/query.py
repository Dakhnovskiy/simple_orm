# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


class Query:

    @property
    def query_str(self):
        query = self.__query_str
        if self.__filter_str:
            query += '\nWHERE ' + self.__filter_str
        return query

    def __init__(self, query_str=None):
        if query_str is None:
            query_str = ''
        self.__query_str = query_str
        self.__filter_str = ''

    def __str__(self):
        return self.query_str

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


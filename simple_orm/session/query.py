# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


class Query:

    def __init__(self, query_str=None):
        if query_str is None:
            query_str = ''
        self.__query_str = query_str

    def __str__(self):
        return self.__query_str

    def filter(self, condition_expression):
        pass


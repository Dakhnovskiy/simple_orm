# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


class BaseField:

    _type_name = None

    def __init__(self, not_null=False, primary_key=False, foreign_key=None, default_value=None):
        """

        :param not_null: является ли поле not null
        :param primary_key: является ли поле первичным ключом
        :param foreign_key: ссылка на внешний ключ
        :param default_value: значение по умолчанию
        """

        self.primary_key = primary_key
        self.not_null = self.primary_key or not_null
        self.foreign_key = foreign_key
        self.default_value = default_value


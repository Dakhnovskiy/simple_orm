# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


class BaseField:

    _type_name = None

    __template_defenition = '{TYPE} {NOT_NULL} {PRIMARY_KEY} {DEFAULT_VALUE}'

    @property
    def type_name(self):
        return self._type_name

    @property
    def __defenition_dict(self):
        return {
            'TYPE': self.type_name,
            'NOT_NULL': 'NOT NULL' if self.not_null else '',
            'PRIMARY_KEY': 'PRIMARY KEY' if self.primary_key else '',
            'DEFAULT_VALUE': 'DEFAULT %s' % self.default_value if self.default_value is not None else '',
        }

    @property
    def defenition(self):
        return self.__template_defenition.format(**self.__defenition_dict)

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

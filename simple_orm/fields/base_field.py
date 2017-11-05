# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


class BaseField:

    _type_name = None

    __template_defenition = '{TYPE} {NOT_NULL} {PRIMARY_KEY} {DEFAULT_VALUE}'

    __template_cmp = '{field_name} {operator} {other}'

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

    @property
    def table_name(self):
        return self.table_class.__table_name__

    @property
    def name(self):
        return self.table_class.get_field_name(self)

    @property
    def full_name(self):
        return self.table_name + '.' + self.name

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
        self.default_value = self.__class__.value(default_value)
        self.table_class = None

    def __repr__(self):
        return self.full_name

    def __fill_template_cmp(self, field_name, operator, other):
        return self.__template_cmp.format(field_name=field_name, operator=operator, other=repr(other))

    def __eq__(self, other):
        return self.__fill_template_cmp(self, '=', other)

    def __ne__(self, other):
        return self.__fill_template_cmp(self, '!=', other)

    def __lt__(self, other):
        return self.__fill_template_cmp(self, '<', other)

    def __gt__(self, other):
        return self.__fill_template_cmp(self, '>', other)

    def __le__(self, other):
        return self.__fill_template_cmp(self, '<=', other)

    def __ge__(self, other):
        return self.__fill_template_cmp(self, '>=', other)

    def set_table_class(self, cls):
        self.table_class = cls

    @staticmethod
    def value(val):
        return val

    @classmethod
    def quoted_value(cls, val):
        return 'NULL' if val is None else cls.value(val)

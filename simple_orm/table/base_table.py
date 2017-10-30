# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from ..fields import BaseField


class BaseTable:

    __table_name__ = None

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

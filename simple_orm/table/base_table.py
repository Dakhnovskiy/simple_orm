# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from ..fields import BaseField


class SetTableClassMeta(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, BaseField):
                attr_value.set_table_class(cls)


class BaseTable(metaclass=SetTableClassMeta):

    __table_name__ = None

    @classmethod
    def get_fields(cls):
        """
        возвращает набор полей таблицы
        :return: список пар [(название колонки, инстанс колонки),..]
        """
        return [(attr, getattr(cls, attr)) for attr in cls.__dict__ if isinstance(getattr(cls, attr), BaseField)]

    @classmethod
    def get_field_name(cls, field_instance):
        """
        :param: field_instance: инстанс поля таблицы
        :return: название поля
        """
        field_name = None
        for attr in cls.__dict__:
            if getattr(cls, attr) is field_instance:
                field_name = attr
                break

        return field_name

    # @classmethod
    # def filter_fields(cls, *fields):
    #     """
    #     Возвращает набор полей таблицы, оставляя только поля из переданных в fields
    #     :comment: Если fields не переданы, то возвращает весь набор полей таблицы
    #     :param fields: Инстансы полей
    #     :return: список пар [(название колонки, инстанс колонки),..]
    #     """
    #     return filter(lambda field: field[1] in fields or not fields, cls.get_fields())

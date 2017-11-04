# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


from .base_field import BaseField


class BooleanField(BaseField):

    _type_name = 'BOOLEAN'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def value(val):
        if val is not None:
            val = 1 if val else 0
        return val

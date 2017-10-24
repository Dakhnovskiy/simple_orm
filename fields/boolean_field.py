# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


from base_field import BaseField


class IntegerField(BaseField):

    _type_name = 'BOOLEAN'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

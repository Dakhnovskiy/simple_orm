# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


from .base_field import BaseField


class TextField(BaseField):

    _type_name = 'TEXT'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

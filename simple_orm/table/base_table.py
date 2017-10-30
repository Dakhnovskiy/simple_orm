# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from ..fields import BaseField


class BaseTable:

    __table_name__ = None

    def get_create_table_script(self):
        pass

    def get_insert_script(self):
        pass

    def get_update_script(self):
        pass

    @classmethod
    def get_fields(cls):
        print([getattr(cls, attr) for attr in cls.__dict__ if isinstance(getattr(cls, attr), BaseField)])

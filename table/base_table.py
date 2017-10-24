# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'


class BaseTable:

    __table_name__ = None

    def get_create_table_script(self):
        pass

    def get_insert_script(self):
        pass

    def get_update_script(self):
        pass

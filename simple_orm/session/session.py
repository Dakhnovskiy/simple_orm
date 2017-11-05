# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

from .query import Query


class Session:
    
    def __init__(self, connect):
        self.__connect = connect
        super().__init__()

    def query(self, *args):
        return Query(*args)
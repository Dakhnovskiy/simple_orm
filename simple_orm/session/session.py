# -*- coding: utf-8 -*-
__author__ = 'Dmitriy.Dakhnovskiy'

import sqlite3
from .query import Query


class Session:
    
    def __init__(self, db):
        super().__init__()
        self.__connect = sqlite3.connect(db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.__connect.close()

    def commit(self):
        self.__connect.commit()

    def query(self, *args):
        return Query(*args, connect=self.__connect)

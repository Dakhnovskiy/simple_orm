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
        """
        Закрыть коннект
        """
        self.__connect.close()

    def commit(self):
        """
        Коммит
        """
        self.__connect.commit()

    def query(self, *args):
        """
        Получить инстанс класса запроса
        :param: args: инстансы класса-поля, класс-таблицы
        :return: инстанс класса запроса
        """
        return Query(*args, connect=self.__connect)

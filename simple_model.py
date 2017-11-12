# -*- coding: utf-8 -*-

from simple_orm.table import BaseTable
from simple_orm.fields import IntegerField, BooleanField, TextField
from simple_orm.session import Session


class City(BaseTable):
    __table_name__ = 'city'

    id = IntegerField(primary_key=True)
    name = TextField(not_null=True)


class User(BaseTable):
    __table_name__ = 'users'

    id = IntegerField(primary_key=True)
    name = TextField(not_null=True)
    id_city = IntegerField(foreign_key=City.id)
    active = BooleanField(not_null=True, default_value=1)


with Session('example.db') as session:

    session.query(City, User).create().execute()
    session.commit()

    city = City(id=1, name='Краснодар')
    city2 = City(id=2, name='Москва')
    city3 = City(id=3, name='Магадан')
    user = User(id=1, name='Вася', id_city=city.id)
    user2 = User(id=2, name='Петя', id_city=city2.id)
    user3 = User(id=3, name='Коля', id_city=city3.id)
    user4 = User(id=4, name='Иван', id_city=city2.id)
    user5 = User(id=5, name='Лёха', id_city=city3.id)
    user6 = User(id=6, name='Степан', id_city=city3.id)

    session.query().insert(city, city2, city3, user, user2, user3, user4, user5, user6).execute()
    session.commit()

    print('\n=======select+autojoin=======')
    for row in session.query(User, City.name).select().join(City).execute():
        print(row)

    session.query(User).update(name='СуперПетя').filter(User.name == 'Петя').execute()
    session.commit()

    session.query(User).delete().filter(User.name == 'Коля').execute()
    session.commit()

    print('\n=======select after update and delete=======')
    for row in session.query(User, City.name).select().join(City).execute():
        print(row)

    print('\n=======select+filter=======')
    for row in session.query(User, City.name).select().join(City).\
            filter(City.name == 'Москва', City.name == 'Магадан', logical_opertor_inner='OR').\
            filter(User.id < 6).execute():
        print(row)

    session.query(User, City).drop().execute()
    session.commit()

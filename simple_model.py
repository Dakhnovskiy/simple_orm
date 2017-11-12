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

    session.query(User).delete().execute()
    session.query(City).delete().execute()
    session.commit()

    city = City(id=1, name='Краснодар')
    city2 = City(id=2, name='Москва')
    user = User(id=1, name='Вася', id_city=city.id)
    user2 = User(id=2, name='Петя', id_city=city2.id)

    session.query().insert(city, city2, user, user2).execute()
    session.commit()

    session.query(User).update(name='СуперПетя').filter(User.name == 'Петя').execute()
    session.commit()

    print('\n=======select+filter=======')
    for row in session.query(User).select().filter(User.name == 'Вася', User.name == 'СуперПетя',
                                                   logical_opertor_inner='OR').filter(User.id < 3).execute():
        print(row)

    print('\n=======select+autojoin=======')
    for row in session.query(User, City.name).select().join(City).execute():
        print(row)

    print(session.query(City, User).select().join(User))

    session.query(User, City).drop().execute()
    session.commit()

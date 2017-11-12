## Пример выборки данных

    with Session('example.db') as session:

        for row in session.query(User, City.name).select().join(City).execute():
            print(row)

        for row in session.query(User, City.name).select().join(City).\
                filter(City.name == 'Москва', City.name == 'Магадан', logical_opertor_inner='OR').\
                filter(User.id < 6).execute():
            print(row)

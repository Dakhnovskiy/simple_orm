## Пример вставки данных

    with Session('example.db') as session:
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

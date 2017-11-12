## Пример обновления данных

    with Session('example.db') as session:
        session.query(User).update(name='СуперПетя').filter(User.name == 'Петя').execute()
        session.commit()

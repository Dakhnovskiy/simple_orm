## Пример удаления данных
    
    with Session('example.db') as session:

        session.query(User).delete().filter(User.name == 'Коля').execute()
        session.commit()

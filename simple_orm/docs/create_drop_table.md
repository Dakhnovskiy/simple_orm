## Пример создания/удаления таблиц 
 
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
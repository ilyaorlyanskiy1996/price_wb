from peewee import *


db = SqliteDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = db

class Orders(BaseModel):
    class Meta:
        db_table = 'Orders'

    user_id = TextField()
    order_brand = TextField()
    order_name = TextField()
    order_id = TextField()
    price = TextField()
    url = TextField()
    original_url = TextField()

if __name__=="__main__":
    db.create_tables([Orders])
else:
    print(f'Импортируется {__name__}')



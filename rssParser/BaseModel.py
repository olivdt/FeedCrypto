from peewee import *

database = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = database

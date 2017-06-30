from peewee import *

database = SqliteDatabase('database.db')

class BaseModel(Model):
    new_item = False

    def update_db(self):
        if self.new_item:
            self.insert()
        else:
            self.update()
        self.save()

    class Meta:
        database = database

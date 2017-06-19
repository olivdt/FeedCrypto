from peewee import *
from rssParser import RssFeed, BaseModel

class SqlHelper(object):

    def open(self):
        BaseModel.database.connect()
        BaseModel.database.create_tables([RssFeed.RssFeed], safe=True)

    def close(self):
        BaseModel.database.close()

    def is_active(self):
        return not (BaseModel.database.is_closed())
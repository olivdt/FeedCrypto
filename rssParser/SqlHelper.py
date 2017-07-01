from peewee import *
from rssParser import Feed, BaseModel

class SqlHelper(object):

    def open(self):
        BaseModel.database.connect()
        BaseModel.database.create_tables([Feed.RssFeed, Feed.Article], safe=True)

    def close(self):
        BaseModel.database.close()

    def is_active(self):
        return not (BaseModel.database.is_closed())
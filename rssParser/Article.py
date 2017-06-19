import newspaper
from peewee import *
from rssParser import RssFeed, BaseModel


class Article(BaseModel.BaseModel):
    """ Article class that can be used with
        any type of feed (RSS/Atom/
    """

    _title = CharField(primary_key=True)
    _url = CharField(unique=True)
    _pub_date = DateTimeField()
    _text = CharField()
    _rssFeed = ForeignKeyField(RssFeed.RssFeed, related_name='articles')

    def __init__(self, title=None, url=None, pubDate=None):
        super(Article, self).__init__()
#        self._title = title if title != None else ''
#        self._url = url if url != None else ''
#        self._pub_date = pubDate if pubDate != None else ''

        self._title = title
        self._url = url
        self._pub_date = pubDate


        if self._title != None and self._url != None and self._pub_date != None:
            self._articleParse = newspaper.Article(self.url)

    @property
    def url(self):
        return self._url if hasattr(self, "_url") else 'No URL'

    @property
    def pub_date(self):
        return self._pub_date if hasattr(self, "_pub_date") else 'No DATE'

    @property
    def authors(self):
        return self._authors if hasattr(self, "_authors") else 'No AUTHORS'

    @property
    def text(self):
        return self._text if hasattr(self, "_text") else 'No TEXT'

    @property
    def downloaded(self):
        return self._downloaded if hasattr(self, "_downloaded") else ' '

    @property
    def title(self):
        return self._title if hasattr(self, "_title") else ' '

    def get_article_contents(self):
        self._parse_article()

    def _parse_article(self):
        self._articleParse.download()
        self._articleParse.parse()

        if self._articleParse.is_parsed:
            self._text = self._articleParse.text
            self._authors = self._articleParse.authors
            self._title = self._articleParse.title
            self._downloaded = True

    def update_db(self):
        self.create()



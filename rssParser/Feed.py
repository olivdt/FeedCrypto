from urllib.request import urlopen, Request
from urllib.parse import urlencode
from xml.etree.cElementTree import fromstring

import newspaper
from dateutil import parser
import datetime
from peewee import *
from peewee import CharField, DateTimeField, ForeignKeyField

from rssParser import BaseModel

class RssFeed(BaseModel.BaseModel):
    """ RSS feed main class
    """

    _title = CharField(primary_key=True)
    _url = CharField()
    _delay = IntegerField()
    _last_download_date = DateTimeField()
    _new_articles_available = BooleanField()

    def __init__(self, title=None, delay=None, url=None):
        super(RssFeed, self).__init__()

        self._title = title
        self._url = url
        self._delay = delay
        self._new_articles_available = False
        self._downloading = False
        self._articles = []

        if title is not None and delay is not None and url is not None:
            self.new_item = True
            self._download_rss_feed()
            self.update_db()

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def delay(self):
        return self._delay

    @property
    def new_articles_available(self):
        return self._new_articles_available

    @property
    def downloading(self):
        return self._downloading

    @property
    def articles(self):
        return self._articles

    def download_new_articles(self):
        if self.new_articles_available:
            for article in self._articles:
                article.get_article_contents()
                print('\n')
                print(str(article.pub_date) + ' ' + article.title)
                print(article.authors)
                print(article.text)

    def _download_rss_feed(self):
        headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://thewebsite.com",
            "Connection": "keep-alive"
        }
        values = {'name': 'Donald Trump',
                  'location': 'New York',
                  'language': 'HTML'}
        data = urlencode(values)
        data = data.encode('ascii')

        req = Request(self.url, data, headers)
        with urlopen(req) as response:
            u = response.read()

        doc = fromstring(u)

        for item in doc.iterfind('channel/item'):
            title = item.findtext('title')
            pub_date_str = item.findtext('pubDate')
            pub_date = parser.parse(pub_date_str)
            link = item.findtext('link')
            if self._articles.__len__() == 0 or pub_date < self._articles[0].pub_date:
                self._articles.append(Article(title, link, pub_date))
                self._new_articles_available = True

        self._articles.sort(key=lambda Article: Article.pub_date, reverse=True)

        for article in self._articles:
            print(str(article.pub_date) + ' ' + article.title)

        self._last_download_date = datetime.datetime.today()


class Article(BaseModel.BaseModel):
    """ Article class that can be used with
        any type of feed (RSS/Atom/
    """

    _title = CharField(primary_key=True)
    _url = CharField(unique=True)
    _pub_date = DateTimeField()
    _text = CharField()
    _rssFeed = ForeignKeyField(RssFeed, related_name='articles')

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

        self.update_db()
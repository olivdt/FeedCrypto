from urllib.request import urlopen, Request
from urllib.parse import urlencode
from xml.etree.cElementTree import fromstring
from dateutil import parser
import datetime
from peewee import *
from rssParser import Article, BaseModel


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
        self._new_feed = False

        self._articles = []

        if title is not None and delay is not None and url is not None:
            self._new_feed = True
            self._download_rss_feed()

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
                self._articles.append(Article.Article(title, link, pub_date))
                self._new_articles_available = True

        self._articles.sort(key=lambda Article: Article.pub_date, reverse=True)

        for article in self._articles:
            print(str(article.pub_date) + ' ' + article.title)

        self._last_download_date = datetime.datetime.today()

    def update_db(self):
        if self._new_feed:
            self.create()
        else:
            self.update()
        self.save()


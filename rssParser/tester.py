from rssParser import Feed, SqlHelper, BaseModel
import datetime

rst = Feed.RssFeed('new', 15, 'http://cointelegraph.com/rss/')
rs = Feed.RssFeed('new1', 15, 'https://letstalkbitcoin.com/rss/feed/blog')
# rs.download_new_articles()
art = Feed.Article('a', 'https://letstalkbitcoin.com/blog/post/the-crypto-show-with-dima-murshik-on-mycelium',
    datetime.datetime.today())
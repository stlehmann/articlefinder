import urllib
import urllib2
import bs4
from articlefinder.article import Article
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.utilities import extract_float

__author__ = 'lehmann'


class MTBNews(AbstractShop):
    def __init__(self):
        super(MTBNews, self).__init__()
        self.name = "MTB News Bikemarket"
        self.url = "http://bikemarkt.mtb-news.de"

    def find_articles(self, search_term):
        data = urllib.urlencode({"q_ft": search_term})
        url = "http://bikemarkt.mtb-news.de/search/index?" + data
        html = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(html)
        for tr in soup("tr"):
            if tr("h3"):
                a = Article()
                a.shop = self
                a.name = tr("h3")[0].a.text
                a.price = extract_float(tr("td", class_="articlePrice")[0].text)
                a.url = self.url + tr("h3")[0]("a")[0]["href"]
                yield a

if __name__ == "__main__":
    shop = MTBNews()
    for a in shop.find_articles("Selle Italia Flite TT"):
        print a.name, a.price, a.url

import urllib
import urllib2
import bs4
from articlefinder.shops.abstractshop import AbstractShop

__author__ = 'lehmann'


class MTBNews(AbstractShop):
    def __init__(self):
        super(MTBNews, self).__init__()
        self.name = "MTB News Bikemarket"
        self.url = "http://www.bikemarkt.mtb-news.de"

    def find_articles(self, search_term):
        data = urllib.urlencode({"q_ft": search_term})
        url = "http://bikemarkt.mtb-news.de/search/index?" + data
        html = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(html)
        tbl = soup("table")[0]
        for row in tbl("tr"):
            print row

if __name__ == "__main__":
    shop = MTBNews()
    shop.find_articles("Umwerfer")

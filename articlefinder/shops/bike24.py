import urllib2
import bs4
import re
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.shops.article import Article

__author__ = 'stefanlehmann'


def _get_productid(link):
    return re.findall("product=(.*);", link)[0]


class Bike24(AbstractShop):
    def __init__(self):
        super(Bike24, self).__init__()
        self.name = "Bike24"
        self.url = "http://www.bike24.net"

    def find_article(self, name):
        name = "+".join(name.split())
        html = urllib2.urlopen("http://www.bike24.net/1.php?content=13&navigation=1&menu=1000%2C4%2C38&search=" + name + ";pitems=50").read()
        soup = bs4.BeautifulSoup(html)
        tbl = soup('table', class_='simpletablefull')
        if not len(tbl):
            return

        headers = tbl[0]("h2")
        for h in headers:
            row = h.parent.parent
            a = Article()
            a.name = h("b")[0].text
            a.url = row("a")[0].get("href")
            a.price = row("td")[2].text
            a.articlenr = _get_productid(a.url)
            yield a

import urllib
import urllib2
import bs4
import re
from articlefinder.shops.article import Article
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.utilities import extract_number, extract_float

__author__ = 'lehmann'


class Conrad(AbstractShop):
    def __init__(self):
        super(Conrad, self).__init__()
        self.name = "Conrad"
        self.url = "http://www.conrad.de/ce/de/"

    def find_articles(self, text):
        text = "+".join(text.split())
        url = urllib.basejoin(self.url, "Search.html?search=" + text)
        html = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(html)

        divs = soup("div", class_="list-product-item teaserClickable")
        for div in divs:
            a = Article()
            name = div("div", class_="name")[0]
            a.name = name("a")[0].text
            a.price = extract_float(div("span", class_="current-price")[0].text)
            a.articlenr = div("div", class_="bestnr")[0].strong.text
            a.shop = self
            yield a

if __name__ == "__main__":
    c = Conrad()
    for a in c.find_articles("Lapp"):
        print a.name, a.price
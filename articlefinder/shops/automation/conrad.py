#-*- coding: utf-8 -*-
import urllib
from articlefinder.article import Article
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.utilities import extract_float

__author__ = 'lehmann'


class Conrad(AbstractShop):
    def __init__(self):
        super(Conrad, self).__init__()
        self.name = "Conrad"
        self.url = "http://www.conrad.de/ce/de/"

    def _get_search_url(self, text):
        """
        Create URL from given search text.

        """
        data = {"search": "+".join(text.split())}
        url_values = urllib.urlencode(data)
        return urllib.basejoin(self.url, "Search.html" + "?" + url_values)

    def find_articles(self, search_term):
        soup = self.get_html_soup(search_term)
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
    for a in c.find_articles("Weidmüller"):
        print a.name, a.price
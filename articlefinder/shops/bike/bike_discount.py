#-*- coding: utf-8 -*-

import urllib
import urllib2
import bs4
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.article import Article
from articlefinder.utilities import extract_float

__author__ = 'lehmann'


class BikeDiscount(AbstractShop):
    def _get_search_url(self, search_term):
        return super(BikeDiscount, self)._get_search_url(search_term)

    def __init__(self):
        super(BikeDiscount, self).__init__()
        self.name = "Bike Discount"
        self.url = "http://www.bike-discount.de"

    def _post_search(self, search_term):
        data = {"query": search_term}
        data = urllib.urlencode(data)
        return urllib2.urlopen(self.url + "/shop/misearch.html", data)

    def find_articles(self, search_term):
        res = self._post_search(search_term)
        html = res.read()
        soup = bs4.BeautifulSoup(html)

        rows = soup("div", class_="pdlistdetails")
        if rows:
            for row in rows:
                a = Article()
                a.shop = self
                a.name = row(class_="name")[0].a.text
                a.brand = row(class_="name")[0].b.text
                a.price = extract_float(row(class_="price")[0].text)
                yield a
        else:
            rows = soup("div", class_="pteaser_smallv small")
            for row in rows:
                a = Article()
                a.shop = self
                a.brand = row.a.text
                a.name = row.a.next_sibling.text
                a.url = self.url + "/" + row("a")[1]["href"]
                a.price = extract_float(row(class_="priceteaser")[0].text)
                yield a


if __name__=="__main__":
    shop = BikeDiscount()
    for a in shop.find_articles("Ultegra"):
        print a.brand, a.name, a.price, a.url
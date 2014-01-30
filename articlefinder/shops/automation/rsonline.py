#-*- coding: utf-8 -*-
import urllib
from articlefinder.article import Article
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.utilities import extract_float, html_to_str

__author__ = 'lehmann'


class RSOnline(AbstractShop):
    def __init__(self):
        super(RSOnline, self).__init__()
        self.name = "RS Online"
        self.url = "http://de.rs-online.com"

    def _get_search_url(self, search_term):
        url = urllib.basejoin(self.url, r"/web/c/")
        search_term = "+".join(search_term.split())
        url = url + "?searchTerm=" + search_term
        return url

    def find_articles(self, search_term):
        soup = self.get_html_soup(search_term)
        div = soup("div", class_="productDescriptionDiv")
        if div:
            #surprisingly only one product
            a = Article()
            div = div[0]
            a.name = html_to_str(div("h1")[0].text)
            a.articlenr = soup("span", class_="keyValue")[0].text
            a.url = self.url + a.articlenr
            a.price = extract_float(soup("span", itemprop="price")[0].text)
            a.brand = soup("span", class_="keyValue")[1].text
            a.shop = self
            yield a

        else:
            tbl = soup("tr", class_="resultRow")
            for row in tbl:
                link = row("a", class_="primarySearchLink")[0]
                a = Article()
                a.name = html_to_str(link.text)
                a.url = self.url + link.get("href")
                a.articlenr = row("a", class_="primarySearchLink")[2].text
                a.brand = row("a", class_="secondarySearchLink")[1].text
                a.price = extract_float(row("span", class_="price right5")[0].text)
                a.brand = row("a", class_="secondarySearchLink")[1].text
                a.shop = self
                yield a

if __name__ == "__main__":
    c = RSOnline()
    for a in c.find_articles("PDU 2,5"):
        print a.name, a.price, a.articlenr

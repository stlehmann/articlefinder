import urllib
import urllib2
import bs4
from articlefinder.shops.article import Article
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.utilities import extract_number, extract_float

__author__ = 'lehmann'


class RSOnline(AbstractShop):
    def __init__(self):
        super(RSOnline, self).__init__()
        self.name = "RS Online"
        self.url = "http://de.rs-online.com"
        self.search_url = urllib.basejoin(self.url, r"/web/c/?sra=oss&r=t&searchTerm=")

    def find_articles(self, text):
        text = "+".join(text.split())
        url = self.search_url + text
        html = urllib2.urlopen(url).read()
        soup = bs4.BeautifulSoup(html)

        div = soup("div", class_="productDescriptionDiv")
        if div:
            #surprisingly only one product
            a = Article()
            div = div[0]
            a.name = div("h1")[0].text
            a.articlenr = soup("span", class_="keyValue")[0].text
            a.url = self.search_url + a.articlenr
            a.price = float(extract_number(soup("span", itemprop="price")[0].text).replace(",", "."))
            a.brand = soup("span", class_="keyValue")[1].text
            a.shop = self
            yield a

        else:
            tbl = soup("tr", class_="resultRow")
            for row in tbl:
                link = row("a", class_="primarySearchLink")[0]
                a = Article()
                a.name = link.text
                a.url = self.url + link.get("href")
                a.articlenr = row("a", class_="primarySearchLink")[2].text
                a.price = extract_float(row("span", class_="price right5")[0].text)
                a.brand = row("a", class_="secondarySearchLink")[1].text
                a.shop = self
                yield a

if __name__ == "__main__":
    c = RSOnline()
    for a in c.find_articles("Kabel"):
        print a.name, a.price, a.articlenr
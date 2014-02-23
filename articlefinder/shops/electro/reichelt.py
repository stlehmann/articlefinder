import urllib
import bs4
from articlefinder.article import Article
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.utilities import extract_float

__author__ = 'Lehmann'


class Reichelt(AbstractShop):
    def __init__(self):
        self.name = "Reichelt"
        self.url = "http://www.reichelt.de"

    def find_articles(self, search_term):
        data = urllib.parse.urlencode({"SEARCH": search_term})
        url = self.url + r"/index.html?&ACTION=446&LA=&0&" + data
        html = urllib.request.urlopen(url).read()
        soup = bs4.BeautifulSoup(html)
        divs = soup("div", class_="al_gallery_article")
        for div in divs:
            a = Article()
            a.name = div("a", class_="al_artinfo_link")[0].text
            a.url = div("a", class_="al_artinfo_link")[0].src
            a.articlenr = div("span", class_="dvartnr")[0].a.text
            a.price = extract_float(div("p", class_="preisRechts")[0].text)
            a.image_url = div("div", class_="al_artlogo")[0].img.get("data-original")
            a.shop = self
            yield a

if __name__ == "__main__":
    reichelt = Reichelt()
    reichelt.find_articles("Batterien AA")

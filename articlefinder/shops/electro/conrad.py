import urllib.request, urllib.parse, urllib.error
import bs4
from articlefinder.article import Article
from articlefinder.shops.abstractshop import AbstractShop
from articlefinder.utilities import extract_float

__author__ = 'lehmann'


class Conrad(AbstractShop):
    """

    """
    def __init__(self):
        super(Conrad, self).__init__()
        self.name = "Conrad"
        self.url = "http://www.conrad.de"

    def find_articles(self, search_term):
        data = urllib.parse.urlencode({"search": search_term})
        url = self.url + "/ce/de/Search.html?" + data
        html = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(html)

        divs = soup("div", class_="list-product-item teaserClickable")
        for div in divs:
            a = Article()
            name = div("div", class_="name")[0]
            a.name = name("a")[0].text
            a.price = extract_float(div("span", class_="current-price")[0].text)
            a.articlenr = div("div", class_="bestnr")[0].strong.text
            a.url = self.url + name("a")[0].get('href')
            a.image_url = div.img.get("src")
            a.shop = self
            yield a

if __name__ == "__main__":
    c = Conrad()
    for a in c.find_articles("Weidmüller"):
        print(a.name, a.price)
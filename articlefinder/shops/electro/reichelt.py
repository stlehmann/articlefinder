import bs4
import urllib
from articlefinder.core.article import Article
from articlefinder.core.shop import Shop
from articlefinder.core.utilities import extract_float


name = "Reichelt"


class Reichelt(Shop):
    def __init__(self):
        self.name = name
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
            a.url = div("a", class_="al_artinfo_link")[0].get("href")
            a.articlenr = div("span", class_="dvartnr")[0].a.text
            try:
               a.price = extract_float(div("p", class_="preisRechts")[0].text)
            except IndexError:
               a.price = 0.0
            a.image_url = div("div", class_="al_artlogo")[0].img.get("data-original")
            a.shop = self
            yield a


def create_shop():
    return Reichelt()

if __name__ == "__main__":
    reichelt = Reichelt()
    reichelt.find_articles("Batterien AA")

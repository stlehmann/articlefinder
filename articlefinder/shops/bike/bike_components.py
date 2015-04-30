import urllib, urllib.parse
import bs4
from articlefinder.core.article import Article
from articlefinder.core.shop import Shop
from articlefinder.core.utilities import extract_float

name = "Bike Components"

class BikeComponents(Shop):
    def __init__(self):
        super().__init__()
        self.name = name
        self.url = "http://www.bike-components.de"

    def find_articles(self, search_term):
        data = urllib.parse.urlencode({"keywords": search_term})
        url = self.url + "/advanced_search_result.php" + "?" + data
        html = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(html)
        items = soup("li", class_=["product", "product last"])
        for li in items:
            a = Article()
            a.name = li.h2.text.strip()
            a.url = urllib.parse.urljoin(self.url, li.a["href"])
            a.price = extract_float(li("span", class_="price")[0].text.strip())
            a.image_url = li.img["src"] if li.img else None
            a.shop = self
            yield a


def create_shop():
    return BikeComponents()


if __name__=="__main__":
    shop = BikeComponents()
    shop.find_articles("Ultegra")

import bs4
import urllib.request, urllib.parse, urllib.error
from articlefinder.core.shop import Shop
from articlefinder.core.article import Article
from articlefinder.core.utilities import extract_float


class BikeDiscount(Shop):
    def _get_search_url(self, search_term):
        return super(BikeDiscount, self)._get_search_url(search_term)

    def __init__(self):
        super(BikeDiscount, self).__init__()
        self.name = "Bike Discount"
        self.url = "http://www.bike-discount.de"

    def find(self, search_term):
        data = urllib.parse.urlencode({"query": search_term})
        url = self.url + "/shop/misearch.html" + "?" + data
        html = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(html)

        rows = soup("div", class_="pdlistdetails")
        if rows:
            for row in rows:
                a = Article()
                a.shop = self
                a.name = row(class_="name")[0].a.text.strip()
                a.brand = row(class_="name")[0].b.text
                a.price = extract_float(row(class_="price")[0].text)
                yield a
        else:
            rows = soup("div", class_="pteaser_smallv small")
            for row in rows:
                a = Article()
                a.shop = self
                a.brand = row.a.text
                a.name = row.a.next_sibling.text.strip()
                a.url = self.url + "/" + row("a")[1]["href"]
                a.price = extract_float(row(class_="priceteaser")[0].text)
                a.image_url = row.img.get("data-original")
                yield a


if __name__=="__main__":
    shop = BikeDiscount()
    for a in shop.find("Ultegra"):
        print((a.brand, a.name, a.price, a.url))
import logging
import bs4
import urllib.request, urllib.parse, urllib.error
from articlefinder.core.shop import Shop
from articlefinder.core.article import Article
from articlefinder.core.utilities import extract_float

name = "Bike Discount"

logger = logging.getLogger('articlefinder.shop.bikediscount')

class BikeDiscount(Shop):
    def _get_search_url(self, search_term):
        return super(BikeDiscount, self)._get_search_url(search_term)

    def __init__(self):
        super(BikeDiscount, self).__init__()
        self.name = name
        self.url = "http://www.bike-discount.de"

    def find(self, search_term):
        # Create url
        data = urllib.parse.urlencode({"query": search_term})
        url = self.url + "/shop/misearch.html" + "?" + data
        logger.info("Open url '%s'" % url)

        # Request HTML
        html = urllib.request.urlopen(url)
        logger.info("url request successful")

        soup = bs4.BeautifulSoup(html)

        items = soup("div", class_="itemPrev")
        logger.info("Found %i items" % len(items))
        for item in items:
            a = Article()
            a.shop = self
            a.name = item('span')[1].text
            a.brand = item('span')[0].text
            a.price = extract_float(item('div', 'price')[0].text)
            a.image_url = self.url + '/' + item('img')[0].get('src')
            a.description = item('div', 'description')[0].text
            yield a


def create_shop():
    return BikeDiscount()


if __name__=="__main__":
    shop = BikeDiscount()
    for a in shop.find("Ultegra"):
        print((a.brand, a.name, a.price, a.url))
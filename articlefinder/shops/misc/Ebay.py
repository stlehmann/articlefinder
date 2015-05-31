import urllib
from urllib.request import Request, urlopen
import bs4
from articlefinder.core.article import Article
from articlefinder.core.shop import Shop
from articlefinder.core.utilities import attr_at_index, extract_float

name = "Ebay"

class Ebay(Shop):
    def __init__(self):
        self.name = name
        self.url = "http://ebay.de"

    def find(self, searchterm):
        data = urllib.parse.urlencode({'_nkw': searchterm})
        url = 'http://www.ebay.de/sch/i.html?' + data
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = bs4.BeautifulSoup(html)

        for item in soup.find_all('li', ('sresult', 'lvresult')):
            article = Article(self)
            article.name = attr_at_index(item('a', 'vip'))
            article.description = attr_at_index(item('div', 'lvsubtitle'))
            article.price = extract_float(
                attr_at_index(item('li', ('lvprice', 'prc'))))
            article.image_url = attr_at_index(item('img'), 0, 'imgurl') or \
                                attr_at_index(item('img'), 0, 'src')
            article.url = attr_at_index(item('a', 'vip'), attr='href')
            yield article


def create_shop():
    return Ebay()


if __name__ == "__main__":
    shop = Ebay()
    for i, article in enumerate(shop.find("Schrumpfschlauch")):
        print(article.image_url)


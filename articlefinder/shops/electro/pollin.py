import urllib
import bs4
import re
from articlefinder.core.article import Article
from articlefinder.core.shop import Shop
from articlefinder.core.utilities import extract_float, attr_at_index

name = "Pollin"


def extract_ordernr(s):
    pattern = re.compile("[0-9]+\s+[0-9]+")
    res = pattern.search(s)
    if res is not None:
        return res.group()


class Pollin(Shop):
    def __init__(self):
        self.name = name
        self.url = "http://pollin.de"

    def find(self, searchterm):

        def is_article_class(x):
            try:
                return 'article' in x
            except TypeError:
                pass

        data = urllib.parse.urlencode({"S_TEXT": searchterm})
        url = self.url + "/shop/suchergebnis.html?" + data
        html = urllib.request.urlopen(url).read()
        soup = bs4.BeautifulSoup(html)

        for div in soup.find_all('div', class_=is_article_class):
            article = Article()
            article.shop = self
            article.name = attr_at_index(div('a'))
            article.description = attr_at_index(div('p'))
            article.ordernr = extract_ordernr(attr_at_index(div('div', 'orderNumber')))
            article.image_url = attr_at_index(div('img'), attr='src')
            article.url = attr_at_index(div('a'), attr='href')
            article.price = extract_float(attr_at_index(div('div', 'price')))
            yield article


def create_shop():
    return Pollin()


if __name__ == "__main__":
    shop = Pollin()
    for article in shop.find("Schrumpfschlauch"):
        print(article, article.url)
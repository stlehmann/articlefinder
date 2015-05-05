import urllib
from urllib.request import Request, urlopen
import bs4
from sqlalchemy.sql.expression import extract
from articlefinder.core.article import Article
from articlefinder.core.shop import Shop
from articlefinder.core.utilities import attr_at_index, extract_float

name = "Amazon"

class Amazon(Shop):
    def __init__(self):
        self.name = name
        self.url = "http://amazon.de"

    def find(self, searchterm):
        data = urllib.parse.urlencode({
            '__mk_de_DE': 'ÅMÅŽÕÑ',
            'url': 'search-alias%3Daps',
            'field-keywords': searchterm})
        url = "http://www.amazon.de/s/ref=nb_sb_noss_2?" + data
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = bs4.BeautifulSoup(html)

        for item in soup.find_all('li', 's-result-item'):
            article = Article(self)
            article.name = attr_at_index(item('h2'))
            article.brand = attr_at_index(
                item('span', 'a-size-small a-color-secondary'), 1)
            article.price = extract_float(attr_at_index(item(
                'span', 'a-size-base a-color-price s-price a-text-bold')))

            try:
                right_column = item('div', 'a-column a-span5 a-span-last')[0]
                article.description = right_column('div')[2]('span')[1].text
            except IndexError:
                pass

            article.url = attr_at_index(item('a'), attr='href')
            article.image_url = attr_at_index(item('img'), attr='src')

            yield article

def create_shop():
    return Amazon()

if __name__ == "__main__":
    shop = Amazon()
    for article in shop.find("Schrumpfschlauch"):
        print(article, article.description)

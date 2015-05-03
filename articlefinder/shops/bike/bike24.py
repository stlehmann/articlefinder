import logging
import bs4
import re
import urllib.parse, urllib.request
from articlefinder.core.shop import Shop
from articlefinder.core.article import Article
from articlefinder.core.utilities import extract_float

name = "Bike24"


logger = logging.getLogger('articlefinder.shops.bike24')


def _get_productid(link):
    if link:
        return re.findall("product=(.*);?", link)[0]


class Bike24(Shop):
    def __init__(self):
        super(Bike24, self).__init__()
        self.name = name
        self.url = "http://www.bike24.net"

    def _get_search_url(self, search_term):

        search_term = "+".join(search_term.split())
        return "http://www.bike24.net/1.php"

    def find(self, search_term):
        # Create URL
        data = urllib.parse.urlencode({"content": "13",
                               "navigation": "1",
                               "search": search_term,
                               "pitems": "50"}, encoding="iso8859-1")
        url = self.url + "/1.php" + "?" + data

        # Make HTML request
        logger.info("Open url '%s'" % url)
        html = urllib.request.urlopen(url)
        logger.info('url request successful')

        # Create BeautifulSoup object
        soup = bs4.BeautifulSoup(html)

        # Get all items
        listitems = soup.find_all('li', ('hit first', 'hit'))
        logger.info("Found %i items", len(listitems))
        for li in listitems:
            a = Article()
            a.shop = self
            a.name = li('a')[1].text
            a.url = self.url + "/" + li('a')[1].get("href")
            a.price = extract_float(li('a', 'price')[0].text)
            a.articlenr = _get_productid(a.url)
            a.image_url = self.url + "/" + li('img')[0].get('src')
            yield a


def create_shop():
    return Bike24()


if __name__ == "__main__":
    shop = Bike24()
    for a in shop.find("Stütze"):
        print((a.name, a.url))
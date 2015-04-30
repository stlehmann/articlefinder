import logging
import bs4
from urllib.error import HTTPError
import urllib.parse, urllib.error
from urllib.request import Request, urlopen
from articlefinder.core.article import Article
from articlefinder.core.utilities import extract_float
from articlefinder.core.shop import Shop


name = "MTB News"
logger = logging.getLogger('articlefinder.shop.mtbnews')


class MTBNews(Shop):
    def __init__(self):
        super(MTBNews, self).__init__()
        self.name = "MTB News Bikemarket"
        self.url = "http://bikemarkt.mtb-news.de"

    def find(self, search_term):
        # Create URL
        data = urllib.parse.urlencode({"q_ft": search_term})
        url = "http://bikemarkt.mtb-news.de/search/index?" + data
        logger.info("Open url  '%s'" % url)

        try:
            # Make HTML Request
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            logger.info("url request successful")

            soup = bs4.BeautifulSoup(html)
            for tr in soup("tr"):
                if tr("h3"):
                    a = Article()
                    a.shop = self
                    a.name = tr("h3")[0].a.text
                    a.price = extract_float(tr("td", class_="articlePrice")[0].text)
                    a.url = self.url + tr("h3")[0]("a")[0]["href"]
                    a.image_url = tr('img')[0].get("src")
                    yield a
        except HTTPError as e:
            logger.error(e)


def create_shop():
    return MTBNews()

if __name__ == "__main__":
    shop = MTBNews()
    for a in shop.find("Selle Italia Flite TT"):
        print((a.name, a.price, a.url))

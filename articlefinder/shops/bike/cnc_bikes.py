import bs4
import urllib.parse, urllib.request
import logging
from articlefinder.core.shop import Shop
from articlefinder.core.article import Article
from articlefinder.core.utilities import extract_float


logger = logging.getLogger("articlefinder.shop.cncbikes")


class CNCBikes(Shop):
    def __init__(self):
        super(CNCBikes, self).__init__()
        self.name = "CNC Bikes"
        self.url = "http://www.cnc-bike.de"

    def _get_search_url(self, search_term):
        return super(CNCBikes, self)._get_search_url(search_term)

    def _search(self, search_term):
        data = urllib.parse.urlencode({"keywords": search_term, "title": "1"}, encoding="iso8859-1")
        url = "http://www.cnc-bike.de/advanced_search_result.php?" + data
        logger.info("Open url '%s'" % url)

        html = urllib.request.urlopen(url)
        logger.info("url request successful")
        soup = bs4.BeautifulSoup(html)

        tbl = soup("table", class_="productListing")[0]
        rows = tbl("tr")[1:]
        logger.info("Found %i items" % len(rows))
        for row in rows:
            a = Article()
            a.shop = self
            a.name = row("a")[1].text
            a.url = row("a")[1]["href"]
            special_price = row("span", class_="productSpecialPrice")
            a.price = extract_float(special_price[0].text
                      if special_price else row("td")[2].text)
            a.image_url = self.url + "/" + row.img.get("src")
            yield a

    def find(self, search_term):
        return self._search(search_term)


if __name__ == "__main__":
    shop = CNCBikes()
    for a in shop.find("Sattelstütze"):
        print((a.name, a.price, a.url))
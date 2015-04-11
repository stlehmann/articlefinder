import urllib.parse
import urllib.request
import re
import bs4
from articlefinder.core.shop import Shop
from articlefinder.core.article import Article
from articlefinder.core.utilities import extract_float


def _get_productid(link):
    if link:
        return re.findall("product=(.*);?", link)[0]


class Bike24(Shop):
    def __init__(self):
        super(Bike24, self).__init__()
        self.name = "Bike24"
        self.url = "http://www.bike24.net"

    def _get_search_url(self, search_term):

        search_term = "+".join(search_term.split())
        return "http://www.bike24.net/1.php"

    def find(self, search_term):
        data = urllib.parse.urlencode({"content": "13",
                               "navigation": "1",
                               "search": search_term,
                               "pitems": "50"}, encoding="iso8859-1")
        url = self.url + "/1.php" + "?" + data
        html = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(html)
        tbl = soup('table', class_='simpletablefull')
        if not len(tbl):
            return

        headers = tbl[0]("h2")
        for h in headers:
            row = h.parent.parent
            a = Article()
            a.shop = self
            a.name = h("b")[0].text
            a.url = self.url + "/" + row("a")[0].get("href")
            a.price = extract_float(row("td")[2].text)
            a.articlenr = _get_productid(a.url)
            a.image_url = self.url + "/" + row.img.get("src")
            yield a

if __name__ == "__main__":
    shop = Bike24()
    for a in shop.find("Stütze"):
        print((a.name, a.url))
import bs4
import urllib
from articlefinder.core.shop import Shop


class Farnell(Shop):
    def __init__(self):
        super().__init__()
        self.name = "Farnell"
        self.url = "http://de.farnell.com"

    def find_articles(self, search_term):
        data = urllib.parse.urlencode({
            "Ntt": search_term,
            "N": "0",
            "Ntk": "description",
            "Ntx": "mode matchall"})
        url = self.url + "/jsp/search/results.jsp?" + data
        print(url)
        html = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(html)

if __name__ == "__main__":
    shop = Farnell()
    shop.find_articles("Siemens Sitop")

import bs4
import urllib.request, urllib.parse, urllib.error
from articlefinder.core.article import Article
from articlefinder.core.shop import Shop
from articlefinder.core.utilities import extract_float


name = "RS Online"


class RSOnline(Shop):
    def __init__(self):
        super(RSOnline, self).__init__()
        self.name = name
        self.url = "http://de.rs-online.com"

    def find_articles(self, search_term):
        data = urllib.parse.urlencode({"searchTerm": search_term})
        url = self.url + "/web/c/?" + data
        html = urllib.request.urlopen(url)
        soup = bs4.BeautifulSoup(html)

        div = soup("div", class_="productDescriptionDiv")
        if div:
            #surprisingly only one product
            a = Article()
            div = div[0]
            a.name = div("h1")[0].text
            a.articlenr = soup("span", class_="keyValue")[0].text
            a.url = self.url + "/web/c/?searchTerm=" + a.articlenrn
            a.price = extract_float(soup("span", itemprop="price")[0].text)
            a.brand = soup("span", class_="keyValue")[1].text
            a.shop = self
            yield a

        else:
            tbl = soup("tr", class_="resultRow")
            for row in tbl:
                link = row("a", class_="primarySearchLink")[0]
                a = Article()
                a.name = link.text
                a.url = self.url + link.get("href")
                a.articlenr = row("a", class_="primarySearchLink")[2].text
                a.brand = row("a", class_="secondarySearchLink")[1].text
                a.price = extract_float(row("span", class_="price right5")[0].text)
                a.brand = row("a", class_="secondarySearchLink")[1].text
                a.image_url = row("img")[0]["src"]
                a.shop = self
                yield a


def create_shop():
    return RSOnline()

if __name__ == "__main__":
    c = RSOnline()
    for a in c.find_articles("Lapp"):
        print(a.name, a.price, a.articlenr)

#-*- coding: utf-8 -*-

__author__ = 'lehmann'

import locale
import sys
import operator
from tabulate import tabulate
from articlefinder.shops.automation import Conrad, RSOnline
from articlefinder.utilities import limit_str

locale.setlocale(locale.LC_ALL, "")
shops = [Conrad(), RSOnline()]


def find(text):
    def _find(text):
        for shop in shops:
            for a in shop.find_articles(text):
                yield a

    articles = _find(text)
    articles = sorted(articles, key=operator.attrgetter("price"))

    tbl = [[article.shop.name,
            limit_str(article.name, 50),
            article.articlenr,
            article.brand,
            locale.currency(article.price, symbol="")]
           for article in articles]

    print tabulate(
        tbl,
        headers=["Shop", "Artikelname", "Artikelnr.", "Marke", "Preis"],
        tablefmt="simple"
    )

#find(sys.argv[1])
find("Verschraubung M16")


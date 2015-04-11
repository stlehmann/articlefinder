from articlefinder.utilities import limit

__author__ = 'lehmann'

import platform
import locale
import operator
from tabulate import tabulate
from articlefinder.finder.finder import Finder

if platform.system()=="Windows":
    locale.setlocale(locale.LC_ALL, "deu_deu")
else:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


class TableDimensionError(Exception):
    def __init__(self):
        self.message = "Header and Attributes lists must have same length."


class TableFinder(Finder):
    def __init__(self):
        super(TableFinder, self).__init__()
        self.tablefmt = "simple"
        self.max_len = 50
        self._headers = []
        self._attributes = []

    def get_attr_value(self, article, attr, max_len=50):
        val = getattr(article, attr)
        if attr == "price":
            return locale.currency(val, symbol=False)
        elif attr == "shop":
            return val.name
        elif attr == "url":
            return val
        else:
            return limit(val, max_len)
    @property
    def headers(self):
        return self._headers

    def headers(self, headers):
        if self._attributes and not len(headers) == len(self._attributes):
            raise TableDimensionError()
        self._headers = headers

    @property
    def visible_attributes(self):
        return self._attributes

    @visible_attributes.setter
    def visible_attributes(self, attributes):
        if not self._headers:
            self._headers = attributes
        else:
            if not len(self.headers)  == len(attributes):
                raise TableDimensionError()
        self._attributes = attributes

    @property
    def column_count(self):
        return len(self._headers)

    def find(self, search_term):
        def _find(search_term):
            print ("-----------------------")
            print ("Browsing Shops")
            print ("-----------------------")
            for shop in self.shops:
                print((shop.name + "..."), end=' ')
                for a in shop.find(search_term):
                    yield a
                print ("Done")
            print ("-----------------------")

        def _get_table():
            for article in articles:
                yield [self.get_attr_value(article, attr) for attr in self._attributes]

        articles = TableFinder.sort(_find(search_term))
        content = _get_table()
        print((tabulate(
            content,
            headers=self._headers,
            tablefmt=self.tablefmt
        )))


__author__ = 'lehmann'

import operator


class SimpleFinder(object):
    def __init__(self):
        super(SimpleFinder, self).__init__()
        self.shops = []

    def find(self, search_term):
        """
        Find articles according to search_term in the shops.
        @rtype: articlefinder.article.Article

        """
        def _find():
            for shop in self.shops:
                for a in shop.find_articles(search_term):
                    yield a
        return list(_find())

    @staticmethod
    def sort(articles, attribute="price"):
        return sorted(articles, key=operator.attrgetter(attribute))
__author__ = 'lehmann'


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
                yield shop.find_articles(search_term)
        return list(_find())
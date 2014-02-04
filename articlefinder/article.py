__author__ = 'stefanlehmann'


class Article(object):
    def __init__(self):
        super(Article, self).__init__()
        self.name = ""
        self.articlenr = ""
        self.price = ""
        self.url = ""
        self.shop = None
        self.unit = 1
        self.brand = ""

    @property
    def shopname(self):
        if self.shop is not None:
            return self.shop.name
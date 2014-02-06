__author__ = 'stefanlehmann'


class Article(object):
    """
    Contains imformation about an Article.

    :ivar name: (basestring) name of the article
    :ivar articlenr: (basestring) article number
    :ivar shop: (AbstractShop) reference to the shop
    :ivar brand: (basestring) name of the brand
    :ivar image_url: (basestring) url to the article image
    :ivar price: (float) price of the article
    :ivar units: (int) number of units in one package

    """

    def __init__(self):
        super(Article, self).__init__()

        self.name = ""
        self.articlenr = ""
        self.price = None
        self.url = ""
        self.shop = None
        self.units = 1
        self.brand = ""
        self.image_url = ""

    @property
    def shopname(self):
        """
        Get the name of the shop.

        """
        if self.shop is not None:
            return self.shop.name
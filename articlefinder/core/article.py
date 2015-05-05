class Article:
    """
    Contains imformation about an Article.

    :ivar name: (basestring) name of the article
    :ivar articlenr: (basestring) article number
    :ivar shop: (AbstractShop) reference to the shop
    :ivar brand: (basestring) name of the brand
    :ivar image_url: (basestring) url to the article image
    :ivar price: (float) price of the article
    :ivar units: (int) number of units in one package
    :ivar QPixmap image: image of the article

    """

    def __init__(self, shop=None):
        self.name = ""
        self.brand = ""
        self.articlenr = ""
        self.ordernr = ""
        self.price = None
        self.url = ""
        self.shop = shop
        self.units = 1
        self.properties = {}
        self.description = ""
        self.image_url = ""
        self.image = None
        self.visible = True

    def __repr__(self):
        return "<Article object " + \
            "name=%s" % self.name + \
            (", brand=%s" % self.brand if self.brand is not "" else "") + \
            (", shop=%s" % self.shop.name if self.shop is not None else "") + \
            (", price=%s" % "%.2f" % self.price if self.price is not None else "") + \
            ">"
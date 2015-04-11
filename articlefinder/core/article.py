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

    def __init__(self):
        self.name = ""
        self.brand = ""
        self.articlenr = ""
        self.ordernr = ""
        self.price = None
        self.url = ""
        self.shop = None
        self.units = 1
        self.properties = {}
        self.notes = ""
        self.image_url = ""
        self.image = None


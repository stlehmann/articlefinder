from io import StringIO
import socket
import urllib.request
from PyQt5.QtGui import QImage, QPixmap

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
        self._image = None
        self.visible = True

    def download_image(self):
        """
        Download the image defined by :attr:`image_url` and store in :attr:`_image`

        """
        if not self.image_url:
            return None
        try:
            response = urllib.request.urlopen(self.image_url, timeout=2).read()
            self._image = QPixmap()
            self._image.loadFromData(response)
        except (socket.timeout, urllib.error.URLError):
            return None

    @property
    def image(self):
        """
        Image of the article.

        :rtype: QPixmap
        """
        if self._image is None:
            self.download_image()

        return self._image

    @property
    def shopname(self):
        """
        Get the name of the shop.

        """
        if self.shop is not None:
            return self.shop.name
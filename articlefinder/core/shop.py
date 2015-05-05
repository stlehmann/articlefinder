import socket
import urllib.request
from urllib.request import Request, urlopen
from PyQt5.QtGui import QPixmap

class Shop:
    """
    Interface for Online-Shops.

    :ivar name: Name of the shop
    :ivar url: base url of the shop

    """
    def __init__(self):
        self.url = ""
        self.name = ""

    def find(self, search_term):
        """
        find_articles(self, search_term)

        Find a list of articles for the given search term.
        Has to be implemented by the derived class.

        :param search_term: term for finding the articles.s
        :type search_term: basestring

        :returns: Generator -- Article objects for the search result

        """
        raise NotImplementedError()

    def download_image(self, image_url):
        """
        Download the image defined by :attr:`image_url` and store in
        :attr:`_image`

        """
        try:
            req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(req).read()
            image = QPixmap()
            image.loadFromData(response)
            return image
        except (socket.timeout, urllib.error.URLError):
            return None
        except ValueError as e:
            return None
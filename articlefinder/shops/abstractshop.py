import urllib.request
import bs4
from articlefinder.utilities import abstractmethod

__author__ = 'stefanlehmann'


class AbstractShop (object):
    """
    Interface for Online-Shops.

    :ivar name: Name of the shop
    :ivar url: base url of the shop

    """
    def __init__(self):
        super(AbstractShop, self).__init__()
        self.url = ""
        self.name = ""

    @abstractmethod
    def find_articles(self, search_term):
        """
        find_articles(self, search_term)

        Find a list of articles for the given search term.
        Has to be implemented by the derived class.

        :param search_term: term for finding the articles.s
        :type search_term: basestring

        :returns: Generator -- Article objects for the search result

        """
        raise NotImplementedError()

    @abstractmethod
    def _get_search_url(self, search_term):
        """
        _get_search_url(self, search_term)

        Create search URL with the given search term.
        Has to be implemented by the derived class.

        """
        raise NotImplementedError()

    def get_html_soup(self, search_term):
        """
        Create search URL and open it. Retrieve the HTML code as a
        Beautifulsoup object.

        :param search_term: term to search for
        :type search_term: basestring
        :returns: bs4.BeautifulSoup

        """
        url = self._get_search_url(search_term)
        html = urllib.request.urlopen(url).read()
        return bs4.BeautifulSoup(html, from_encoding="utf-8")
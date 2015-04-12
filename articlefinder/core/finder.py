import time
import logging
import operator
from queue import Queue
from threading import Thread
from articlefinder.shops.bike.bike24 import Bike24
from articlefinder.shops.bike.bike_discount import BikeDiscount
from articlefinder.shops.bike.cnc_bikes import CNCBikes
from articlefinder.shops.bike.mtb_news import MTBNews


logger = logging.getLogger("articlefinder.core.finder")


class Finder(object):
    def __init__(self, shops=[]):
        super(Finder, self).__init__()
        self.shops = shops

    def find(self, search_term):
        """
        Search for search_term in all shops and return an Iterator for
        the found Article objects.

        """
        def download(shop, res_queue):
            def _download():
                for a in shop.find(search_term):
                    print(a)
                    res_queue.put(a)
            return _download()

        queue = Queue()
        threads = []
        for shop in self.shops:
            t = Thread(target=download, args=(shop,queue))
            t.start()
            threads.append(t)

        waiting = True
        while(waiting):
            b = False
            for thread in threads:
                if thread.is_alive():
                    b = True
                    break
            waiting = b

        while not queue.empty():
            yield queue.get()


    @staticmethod
    def sort(articles, attribute="price"):
        return sorted(articles, key=operator.attrgetter(attribute))


if __name__ == "__main__":
    import articlefinder.core.logger
    searchterm = "Shimano Ultegra"
    finder = Finder([Bike24(), BikeDiscount(), CNCBikes(), MTBNews()])

    logger.info("Starting search for %s" % searchterm)

    t1 = time.time()
    articles = list(finder.find(searchterm))
    diff = time.time() - t1

    logger.info("Search done in %.3fs" % diff)
__author__ = 'stefanlehmann'


class AbstractShop (object):
    def __init__(self):
        super(AbstractShop, self).__init__()
        self.url = ""
        self.name = ""

    def find_article(self, text):
        raise NotImplementedError()
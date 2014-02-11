#! python3
import io
from operator import indexOf
from PIL import Image
from urllib.request import urlretrieve, urlopen
from PIL.ImageTk import PhotoImage
from articlefinder.finder.simple_finder import SimpleFinder
from articlefinder.shops.automation.conrad import Conrad
from articlefinder.shops.automation.rsonline import RSOnline
from articlefinder.tk.hyperlinks import HyperlinkManager
from articlefinder.utilities import limit

__author__ = 'lehmann'

from articlefinder.tk.tk_finder import TkFinder, get_char_count


class MyFinder(SimpleFinder):
    def __init__(self, text_widget):
        super(MyFinder, self).__init__()
        self.text_widget = text_widget
        self.hyperlinks = HyperlinkManager(self.text_widget)

    def find(self, search_term):
        articles = SimpleFinder.sort(SimpleFinder.find(self, search_term))
        for i, article in enumerate(articles, start=1):
            self.text_widget.insert(
                "end",
                limit(article.shop.name,
                          get_char_count(articles, column="shopname") + 1)
            )
            self.text_widget.insert(
                "end",
                limit(article.name,
                          get_char_count(articles, column="name") + 1)
            )
            self.text_widget.insert("end", article.articlenr,
                                    self.hyperlinks.add(article.url))
            price = format("%0.2f") % article.price
            self.text_widget.insert("end", price.rjust(10))
            self.text_widget.insert("end", "\n")


class ElectroTkFinder(TkFinder):
    def __init__(self, shops):
        super(ElectroTkFinder, self).__init__(shops)
        self.finder = MyFinder(self.output)
        self.finder.shops = shops

w = ElectroTkFinder([RSOnline(), Conrad()])
w.mainloop()

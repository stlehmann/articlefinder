import sys
from tkinter import *
from tkinter import ttk
from articlefinder.finder import SimpleFinder
from articlefinder.shops.bike.bike24 import Bike24
from articlefinder.shops.bike.bike_discount import BikeDiscount
from articlefinder.shops.bike.cnc_bikes import CNCBikes
from articlefinder.shops.bike.mtb_news import MTBNews
from articlefinder.tk.hyperlinks import HyperlinkManager
from articlefinder.utilities import limit_str


__author__ = 'stefanlehmann'
def get_char_count(articles, column="name"):
        count = 0
        for article in articles:
            x = len(getattr(article, column))
            if x > count:
                count = x
        return count

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
                limit_str(article.shop.name,
                          get_char_count(articles, column="shopname") + 1)
            )
            self.text_widget.insert(
                "end",
                limit_str(article.name,
                          get_char_count(articles, column="name") + 1)
            )
            self.text_widget.insert("end", limit_str(format("%0.2f€") % article.price, 10))
            self.text_widget.insert("end", "Link", self.hyperlinks.add(article.url))
            self.text_widget.insert("end", "\n")



def search(*args):
    output.delete("1.0", "end")
    text = search_term.get()
    finder.find(text)
    output.insert(END, search_term.get())
    root.update_idletasks()


#GUI objects
root = Tk()
root.title("Bike Parts Finder")

output = Text(root)
output.pack(side=BOTTOM, fill=BOTH, expand=1)
output.config(wrap=NONE)

search_label = ttk.Label(root, text="Suchtext:")
search_label.pack(side=LEFT)

search_term = StringVar()
search_entry = ttk.Entry(root, textvariable=search_term)
search_entry.pack(side=LEFT)

search_button = ttk.Button(root, text="Suchen", command=search)
search_button.pack(side=RIGHT)

#The Finder object
finder = MyFinder(output)
finder.shops = [Bike24(), BikeDiscount(), CNCBikes(), MTBNews()]

search_entry.focus()
root.bind("<Return>", search)
root.mainloop()

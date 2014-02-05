#! python3

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


root = Tk()
root.title("Bike Parts Finder")

#Scrollbars
yscrollbar = Scrollbar(root)
yscrollbar.grid(column=4, row=1, sticky=(N, S))
xscrollbar = Scrollbar(root, orient=HORIZONTAL)
xscrollbar.grid(column=0, row=2, columnspan=3, sticky=(W, E))

#Output Textbox
output = Text(root)
output.grid(column=0, row=1, columnspan=3, sticky=(N, S, W, E))
output.config(wrap=NONE)
output.config(yscrollcommand=yscrollbar.set)
yscrollbar.config(command=output.yview)
output.config(xscrollcommand=xscrollbar.set)
xscrollbar.config(command=output.xview)

#Label
search_label = ttk.Label(root, text="Suchtext:")
search_label.grid(column=0, row=0)

#Entry
search_term = StringVar()
search_entry = ttk.Entry(root, textvariable=search_term)
search_entry.grid(column=1, row=0, sticky=(W, E))

#Button
search_button = ttk.Button(root, text="Suchen", command=search)
search_button.grid(column=2, row=0)

#The Finder object
finder = MyFinder(output)
finder.shops = [Bike24(), BikeDiscount(), CNCBikes(), MTBNews()]

search_entry.focus()
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=0)
root.rowconfigure(1, weight=1)
root.bind("<Return>", search)
root.mainloop()

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


class TkFinder(Tk, object):
    def __init__(self, shops=[]):
        super(TkFinder, self).__init__()
        self.shops = shops
        self.title("Article Finder")

        #Scrollbars
        self.yscrollbar = Scrollbar(self)
        self.yscrollbar.grid(column=4, row=1, sticky=(N, S))
        self.xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.xscrollbar.grid(column=0, row=2, columnspan=3, sticky=(W, E))

        #Output Textbox
        self.output = Text(self)
        self.output.grid(column=0, row=1, columnspan=3, sticky=(N, S, W, E))
        self.output.config(wrap=NONE)
        self.output.config(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.config(command=self.output.yview)
        self.output.config(xscrollcommand=self.xscrollbar.set)
        self.xscrollbar.config(command=self.output.xview)

        #Label
        self.search_label = ttk.Label(self, text="Suchtext:")
        self.search_label.grid(column=0, row=0)

        #Entry
        self.search_term = StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_term)
        self.search_entry.grid(column=1, row=0, sticky=(W, E))

        #Button
        search_button = ttk.Button(self, text="Suchen", command=self.search)
        search_button.grid(column=2, row=0)

        #The Finder object
        self.finder = MyFinder(self.output)
        self.finder.shops = self.shops

        self.search_entry.focus()
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)
        self.bind("<Return>", self.search)

    def search(self, *args):
        self.output.delete("1.0", "end")
        text = self.search_term.get()
        self.finder.find(text)
        self.output.insert(END, self.search_term.get())

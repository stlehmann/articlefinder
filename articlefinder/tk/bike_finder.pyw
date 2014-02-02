import sys
from tkinter import *
from tkinter import ttk
from articlefinder.finder import SimpleFinder
from articlefinder.shops.bike.bike24 import Bike24
from articlefinder.shops.bike.bike_discount import BikeDiscount
from articlefinder.shops.bike.cnc_bikes import CNCBikes
from articlefinder.shops.bike.mtb_news import MTBNews


__author__ = 'stefanlehmann'


class MyFinder(SimpleFinder):
    def __init__(self, text_widget):
        super(MyFinder, self).__init__()
        self.text_widget = text_widget

    def find(self, search_term):
        articles = SimpleFinder.find(self, search_term)
        for article in articles:
            self.text_widget.insert("end", "\n" + article.name)



def search(*args):
    text = search_term.get()
    finder.find(text)
    output.insert(END, search_term.get())
    root.update_idletasks()


root = Tk()
root.title("Bike Parts Finder")

search_term = StringVar()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, S, E))
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.columnconfigure(3, weight=2)
mainframe.rowconfigure(0, weight=0)
mainframe.rowconfigure(1, weight=2)
root.rowconfigure(0,weight=1)
root.columnconfigure(0, weight=1)

search_label = ttk.Label(mainframe, text="Suchtext:").grid(column=0, row=0)
search_entry = ttk.Entry(mainframe, textvariable=search_term)
search_entry.grid(column=1, row=0)
search_button = ttk.Button(mainframe, text="Suchen", command=search).grid(column=2, row=0)

output = Text(mainframe)
output.grid(column=0, row=1, columnspan=4, sticky=(N, W, S, E))
output.tag_config("a", foreground="blue", underline=1)
scrollbar = Scrollbar(mainframe)
scrollbar.grid(column=0, row=2, columnspan=4)
scrollbar.config(command=output.yview)
output.config(yscrollcommand=scrollbar.set)

#The Finder object
finder = MyFinder(output)
finder.shops = [Bike24(), BikeDiscount(), CNCBikes(), MTBNews()]

search_entry.focus()
root.bind("<Return>", search)
root.mainloop()

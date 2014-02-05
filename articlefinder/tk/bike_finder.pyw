from articlefinder.shops.bike.bike24 import Bike24
from articlefinder.shops.bike.bike_discount import BikeDiscount
from articlefinder.shops.bike.cnc_bikes import CNCBikes
from articlefinder.shops.bike.mtb_news import MTBNews
from articlefinder.tk.tk_finder import TkFinder

__author__ = 'lehmann'


w = TkFinder([Bike24(), BikeDiscount(), CNCBikes(), MTBNews()])
w.mainloop()
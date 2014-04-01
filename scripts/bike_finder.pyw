#! python3
from articlefinder.shops.bike.bike24 import Bike24
from articlefinder.shops.bike.bike_discount import BikeDiscount
from articlefinder.shops.bike.cnc_bikes import CNCBikes
from articlefinder.shops.bike.mtb_news import MTBNews
from articlefinder.qt import mainwindow

__author__ = 'lehmann'


mainwindow.run([Bike24(), BikeDiscount(), MTBNews(), CNCBikes()],
               title="Bike Finder")
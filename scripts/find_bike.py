#-*- coding: utf-8 -*-

__author__ = 'lehmann'

import sys
from articlefinder.finder.table_finder import TableFinder
from articlefinder.shops.bike import Bike24, BikeDiscount, CNCBikes

finder = TableFinder()
finder.shops = [Bike24(), BikeDiscount(), CNCBikes()]
finder.visible_attributes = ["shop", "name", "brand", "price"]
#find(sys.argv[1])
finder.find("Ultegra Umwerfer")


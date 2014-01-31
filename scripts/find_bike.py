__author__ = 'lehmann'

import sys
from articlefinder.finder.table_finder import TableFinder
from articlefinder.shops.bike import Bike24, BikeDiscount, CNCBikes, MTBNews

finder = TableFinder()
finder.shops = [Bike24(), BikeDiscount(), CNCBikes(), MTBNews()]
finder.visible_attributes = ["shop", "name", "brand", "price"]

finder.find(sys.argv[1])


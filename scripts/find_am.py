__author__ = 'lehmann'

import sys
from articlefinder.finder.table_finder import TableFinder
from articlefinder.shops.automation import Conrad, RSOnline

finder = TableFinder()
finder.shops = [Conrad(), RSOnline()]
finder.visible_attributes = ["shop", "name", "brand", "price"]
finder.find(sys.argv[1])


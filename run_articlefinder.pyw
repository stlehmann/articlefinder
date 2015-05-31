
#! python3
import articlefinder.core.logger
import logging
from articlefinder.shops.bike.bike24 import Bike24
from articlefinder.shops.bike.bike_discount import BikeDiscount
from articlefinder.shops.bike.cnc_bikes import CNCBikes
from articlefinder.shops.bike.mtb_news import MTBNews
from articlefinder.shops.electro.conrad import Conrad
from articlefinder.shops.electro.reichelt import Reichelt
from articlefinder.shops.electro.rsonline import RSOnline
from articlefinder.gui import mainwindow



# ====================
# Starting Application
# ====================
logger = logging.getLogger("articlefinder")
logger.info('Starting Application')
mainwindow.run()
logger.info('Terminating Application')
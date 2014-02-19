#! python3
from articlefinder.shops.electro.conrad import Conrad
from articlefinder.shops.electro.reichelt import Reichelt
from articlefinder.shops.electro.rsonline import RSOnline

__author__ = 'lehmann'

from articlefinder.qt import mainwindow

mainwindow.run([Conrad(), RSOnline(), Reichelt()])
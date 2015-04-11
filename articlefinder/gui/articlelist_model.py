from urllib.request import urlretrieve, urlopen
from PyQt5.QtCore import QModelIndex, Qt, QVariant, \
    QAbstractTableModel, QSize, QByteArray
import operator
from PyQt5.QtGui import QBrush, QFontMetrics, QFont, QImage, QPixmap

__author__ = 'stefanlehmann'

COLUMN_COUNT = 4
IMAGE, NAME, PRICE, SHOP = range(COLUMN_COUNT)


class ArticleListModel(QAbstractTableModel):
    """
    Model for listing the articles.

    :ivar list articles: list of articles, result of a search

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.articles = []
        self.visible_articles = []
        self.table = None
        self._sort_column = 2
        self._sort_order = Qt.AscendingOrder

    def columnCount(self, index=QModelIndex()):
        return COLUMN_COUNT

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() <= len(self.visible_articles)):
            return QVariant()

        article = self.visible_articles[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == IMAGE:
                return ""
            if column == NAME:
                return article.name
            if column == PRICE:
                return "%0.2f€" % article.price
            if column == SHOP:
                return article.shop.name

        if role == Qt.TextAlignmentRole:
            if column == IMAGE:
                return Qt.AlignCenter | Qt.AlignVCenter
            if column == PRICE:
                return Qt.AlignRight | Qt.AlignVCenter
            else:
                return Qt.AlignLeft | Qt.AlignVCenter

        if role == Qt.ForegroundRole:
            if column == NAME:
                return QBrush(Qt.blue)

        if role == Qt.SizeHintRole:
            if column == NAME:
                fm = QFontMetrics(QFont(self.data(index, Qt.FontRole)))
                w = fm.width(article.name)
                w = w if w < 500 else 250
                h = fm.height()
                return QSize(w, h)

        if role == Qt.DecorationRole:
            if column == IMAGE:
                if article.image is None:
                    return QVariant()
                #Scale the image to cell size if larger
                #----------------------------------------------------
                row_height = self.table.rowHeight(index.row())
                column_width = self.table.columnWidth(index.column())
                img = article.image
                #scale height
                if img.height() > row_height:
                    img = img.scaledToHeight(row_height)
                #scale width
                if img.width() > column_width:
                    img = img.scaledToWidth(column_width)
                return img
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == NAME:
                    return self.tr("Name")
                if section == PRICE:
                    return self.tr("Price")
                if section == SHOP:
                    return self.tr("Shop")
            else:
                return QVariant(int(section + 1))
        else:
            return QVariant()

    def refresh(self):
        self.beginResetModel()
        self.visible_articles = [a for a in self.articles if a.visible]
        self.sort(self._sort_column, self._sort_order)
        self.endResetModel()

    def rowCount(self, index=QModelIndex()):
        return len(self.visible_articles)

    def sort(self, column, order=Qt.AscendingOrder):
        self._sort_column = column
        self._sort_order = order
        self.beginResetModel()
        attribute = ['name', 'name', 'price', 'shopname']
        self.visible_articles = sorted(self.visible_articles,
                               key=operator.attrgetter(attribute[column]),
                               reverse=order == Qt.DescendingOrder)
        self.endResetModel()
from PyQt5.QtCore import QModelIndex, Qt, QVariant, \
    QAbstractTableModel
import operator

__author__ = 'stefanlehmann'

NAME, ARTICLE_NR, PRICE, SHOP = range(4)


class ArticleListModel(QAbstractTableModel):
    """
    Model for listing the articles.

    :ivar list articles: list of articles, result of a search

    """


    def __init__(self, parent=None):
        super().__init__(parent)
        self.articles = []

    def rowCount(self, index=QModelIndex()):
        return len(self.articles)

    def columnCount(self, index=QModelIndex()):
        return 4

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() <= len(self.articles)):
            return QVariant()

        article = self.articles[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == NAME :
                return article.name
            if column == ARTICLE_NR:
                return article.articlenr
            if column == PRICE:
                return "%0.2f€" % article.price
            if column == SHOP:
                return article.shopname

        if role == Qt.TextAlignmentRole:
            if column == PRICE:
                return Qt.AlignRight
            else:
                return Qt.AlignLeft

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == NAME:
                    return "name"
                if section == ARTICLE_NR:
                    return "articlenr"
                if section == PRICE:
                    return "price"
                if section == SHOP:
                    return "shop"
            else:
                return QVariant(int(section + 1))
        else:
            return QVariant()

    def sort(self, column, order=Qt.AscendingOrder):
        self.beginResetModel()
        attribute = ['name', 'articlenr', 'price', 'shop']
        self.articles = sorted(self.articles,
                               key=operator.attrgetter(attribute[column]),
                               reverse=order == Qt.DescendingOrder)
        self.endResetModel()
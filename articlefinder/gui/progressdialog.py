"""
A Dialog showing the progress of downloading article information.

"""
import logging
from PyQt5.QtCore import QAbstractTableModel, QThread, pyqtSignal, QModelIndex, \
    Qt
from PyQt5.QtGui import QPainter, QResizeEvent
from PyQt5.QtWidgets import QDialog, QTableView, QVBoxLayout, QPushButton, \
    QStyleOptionViewItem, QStyleOptionProgressBar, QStyledItemDelegate, QStyle, \
    QApplication, QStyleOptionProgressBar

logger = logging.getLogger("articlefinder.progressdialog")


class WorkerThread(QThread):
    """
    Thread for doing all the work:
        * finding the articles in the shops
        * downloading images

    """
    progress = pyqtSignal(int, int, str, name="progress")

    def __init__(self, shop):
        super(WorkerThread, self).__init__()
        self._cancel = False
        self.shop = shop
        self.searchterm = ""
        self.articles = []

    def run(self):
        def _find():
            self.progress.emit(0, 0, self.tr("Searching shop for articles"))
            try:
                for a in self.shop.find(self.searchterm):
                    yield a
                    if self._cancel:
                        return
            except NotImplementedError as e:
                logger.warning(
                    "'Find' function not implemented for shop '%s'."
                    % self.shop.name)
            except TypeError as e:
                logger.debug("No results in shop '%s'." % self.shop.name)

        self._cancel = False
        self.articles = list(_find())
        self._cancel = False
        for i, article in enumerate(self.articles):
            if self._cancel:
                return
            self.progress.emit(
                i, len(self.articles),
                self.tr("Loading image %i of %i") % (i, len(self.articles)))
            article.image = article.shop.download_image(article.image_url)
        self.progress.emit(0, 0, "Found %i articles" % len(self.articles))

    def quit(self):
        self._cancel = True


class ProgressbarDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex):

        if index.column() == 2:
            style = QStyleOptionProgressBar()
            style.rect = option.rect
            style.minimum = 0
            style.maximum = 100
            style.progress = index.data(Qt.UserRole)

            if style.progress == 0:
                QStyledItemDelegate.paint(self, painter, option, index)
            else:
                QApplication.style().drawControl(
                    QStyle.CE_ProgressBar, style, painter)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)


class ThreadItem():
    def __init__(self, model, thread: WorkerThread):
        self.thread = thread
        self.thread.progress.connect(self._set_progress)
        self.message = ""
        self.model = model
        self.progress = 0

    def name(self):
        return self.thread.shop.name

    def _set_progress(self, current, count, message):
        row = self.model.items.index(self)
        index0 = self.model.index(row, 1, QModelIndex())
        index1 = self.model.index(row, 2, QModelIndex())
        self.message = message
        self.progress = 100 * current / count if count > 0 else 0
        self.model.dataChanged.emit(index0, index1, [Qt.DisplayRole])


class ProgressModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []
        self.columns = [
            self.tr("shop"),
            self.tr("progress"),
            self.tr(""),
        ]

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return

        item = self.items[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return item.name()
            elif index.column() == 1:
                return item.message

        elif role == Qt.UserRole:
            return item.progress

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, QModelIndex_parent=QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columns[section]

    def add_thread(self, thread: WorkerThread):
        self.items.append(ThreadItem(self, thread))

    def set_searchterm(self, searchterm: str):
        for threaditem in self.items:
            thread = threaditem.thread
            thread.searchterm = searchterm


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__active_threads = 0
        self.__shops = []

        # TableView
        self.model = ProgressModel()
        self.tableview = QTableView()
        self.tableview.setModel(self.model)
        self.tableview.setItemDelegateForColumn(2, ProgressbarDelegate())

        # Cancel Button
        self.cancelButton = QPushButton(self.tr("Cancel"))
        self.cancelButton.pressed.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableview)
        layout.addWidget(self.cancelButton)
        self.setLayout(layout)

        self.tableview.setColumnWidth(0, 200)
        self.tableview.setColumnWidth(1, 210)
        self.tableview.setColumnWidth(2, 100)
        self.resize(630, 260)

    @property
    def shops(self):
        return self.__shops

    @shops.setter
    def shops(self, shops: []):
        self.model.beginResetModel()
        self.model.items.clear()
        for shop in shops:
            thread = WorkerThread(shop)
            self.model.add_thread(thread)
        self.model.endResetModel()

    def run_search(self, searchterm):
        self.model.set_searchterm(searchterm)
        for threaditem in self.model.items:
            thread = threaditem.thread
            thread.finished.connect(self.__thread_finished)
            self.__active_threads += 1
            thread.start()

    def __thread_finished(self):
        self.__active_threads -= 1

        if self.__active_threads == 0:
            self.close()

    @property
    def articles(self):
        articles = []
        for threaditem in self.model.items:
            articles.extend(threaditem.thread.articles)
        return articles

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    import articlefinder.shops.bike.bike24 as bike24
    import articlefinder.shops.bike.cnc_bikes as cncbikes
    import articlefinder.shops.bike.bike_discount as bikediscount
    import articlefinder.shops.bike.mtb_news as mtbnews

    app = QApplication(sys.argv)
    dlg = ProgressDialog()

    dlg.shops = [
        bike24.create_shop(),
        cncbikes.create_shop(),
        bikediscount.create_shop(),
        mtbnews.create_shop()
    ]

    dlg.run_search("Shimano")
    dlg.exec_()
    articles = dlg.articles
    print(articles)
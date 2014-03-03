#! python3

import os
import sys
import webbrowser
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTranslator, QThread, pyqtSignal, QCoreApplication, \
    QSettings
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, \
    QGridLayout, QPushButton, QTableView, QWidget, QListWidget, \
    QSplitter, QListWidgetItem, QProgressDialog, QToolBox, QDockWidget, \
    QMainWindow
from articlefinder.qt.articlelist_model import ArticleListModel, PRICE, NAME
from articlefinder.shops.bike.bike24 import Bike24
from articlefinder.shops.bike.bike_discount import BikeDiscount
from articlefinder.shops.bike.cnc_bikes import CNCBikes
from articlefinder.shops.bike.mtb_news import MTBNews

__author__ = 'stefanlehmann'

WINDOW_STATE_SETTING = "WindowState"
WINDOW_GEOMETRY_SETTING = "WindowGeometry"


class WorkerThread(QThread):
    """
    Thread for doing all the work:
        * finding the articles in the shops
        * downloading images

    """
    progress = pyqtSignal(int, int, str, name="progress")

    def __init__(self):
        super(WorkerThread, self).__init__()
        self._cancel = False
        self.shops = []
        self.search_term = ""
        self.articles = []

    def run(self):
        def _find():
            for i, shop in enumerate(self.shops):
                self.progress.emit(i, len(self.shops), "Suche Artikel bei %s" % shop.name)
                for a in shop.find_articles(self.search_term):
                    yield a

        self.articles = list(_find())
        for i, article in enumerate(self.articles):
            self.progress.emit(i, len(self.articles), "Bilder herunterladen")
            article.download_image()


class CentralWidget(QWidget):
    def __init__(self):
        super(CentralWidget, self).__init__()

        #Search label and LineEdit
        self.searchLabel = QLabel(self.tr("Search term:"))
        self.searchLineEdit = QLineEdit()
        self.searchLabel.setBuddy(self.searchLineEdit)

        #Search Button
        self.searchButton = QPushButton(self.tr("Search"))

        #Results
        self.resultTable = QTableView()
        self.resultTable.setSortingEnabled(True)
        self.resultTable.setMouseTracking(True)

        #Layout
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.searchLabel, 0, 0)
        self.layout().addWidget(self.searchLineEdit, 0, 1)
        self.layout().addWidget(self.searchButton, 0, 2)
        self.layout().addWidget(self.resultTable, 1, 0, 1, 3)


class SuppliersDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(SuppliersDockWidget, self).__init__(parent)
        self.setObjectName("SuppliersDockWidget")
        self.setWindowTitle(self.tr("Supplier list"))
        self.suppliersListWidget = QListWidget()
        self.setWidget(self.suppliersListWidget)


class MainWindow(QMainWindow):
    def __init__(self, shops, parent=None):
        super().__init__(parent)

        self.worker = WorkerThread()
        self.worker.finished.connect(self.finished)
        self.worker.progress.connect(self.progress)
        self.progressDlg = QProgressDialog()
        self.progressDlg.canceled.connect(self.worker.quit)
        self.suppliers = shops
        self.model = ArticleListModel()

        self.setCentralWidget(CentralWidget())
        self.centralWidget().resultTable.setModel(self.model)
        self.centralWidget().searchLineEdit.returnPressed.connect(self.search)
        self.centralWidget().resultTable.clicked.connect(self.open_url)
        self.centralWidget().searchButton.pressed.connect(self.search)
        self.centralWidget().resultTable.mouseMoveEvent = self.resultTable_mouseMove

        #supplier list
        self.suppliersDockWidget = SuppliersDockWidget()
        self.suppliersListWidget = self.suppliersDockWidget.suppliersListWidget
        self.suppliersListWidget.itemChanged.connect(self.filter_checked_suppliers)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.suppliersDockWidget)

        self.fill_supplier_list()
        try:
            self.restoreState(QSettings().value(WINDOW_STATE_SETTING))
            self.restoreGeometry(QSettings().value(WINDOW_GEOMETRY_SETTING))
        except (AttributeError, TypeError):
            self.resize(600, 800)

    def closeEvent(self, event):
        QSettings().setValue(WINDOW_STATE_SETTING, self.saveState())
        QSettings().setValue(WINDOW_GEOMETRY_SETTING, self.saveGeometry())
        QMainWindow.closeEvent(self, event)

    def fill_supplier_list(self):
        self.suppliersListWidget.clear()
        for s in self.suppliers:
            item = QListWidgetItem(s.name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            item.setData(Qt.UserRole, s)
            self.suppliersListWidget.addItem(item)

    def filter_checked_suppliers(self):
        for row in range(self.suppliersListWidget.count()):
            item = self.suppliersListWidget.item(row)
            shop = item.data(Qt.UserRole)
            for a in self.model.articles:
                if a.shopname == shop.name:
                    a.visible = item.checkState()
        self.model.refresh()

    def finished(self):
        self.progressDlg.close()
        self.model.beginResetModel()
        self.model.articles = self.worker.articles
        self.filter_checked_suppliers()
        self.model.refresh()
        self.model.endResetModel()

        self.centralWidget().resultTable.sortByColumn(PRICE, Qt.AscendingOrder)
        self.centralWidget().resultTable.resizeColumnsToContents()
        self.centralWidget().resultTable.resizeRowsToContents()

    def open_url(self, event):
        index = self.centralWidget().resultTable.currentIndex()
        if index.isValid():
            if index.column() == NAME:
                article = self.model.visible_articles[index.row()]
                webbrowser.open_new_tab(article.url)

    def progress(self, i, max, shopname):
        self.progressDlg.setMaximum(max)
        self.progressDlg.setLabelText(shopname)
        self.progressDlg.setValue(i)

    def resultTable_mouseMove(self, event):
        index = self.centralWidget().resultTable.indexAt(event.pos())
        if not index.isValid():
            self.centralWidget().resultTable.unsetCursor()

        if index.column() == NAME:
            self.centralWidget().resultTable.setCursor(Qt.PointingHandCursor)
        else:
            self.centralWidget().resultTable.unsetCursor()

    def search(self):
        def _get_suppliers():
            for row in range(self.suppliersListWidget.count()):
                item = self.suppliersListWidget.item(row)
                yield item.data(Qt.UserRole)

        self.worker.shops = list(_get_suppliers())
        self.worker.search_term = self.centralWidget().searchLineEdit.text()
        self.progressDlg.setMinimum(0)
        self.progressDlg.setMaximum(len(self.worker.shops))
        self.progressDlg.setModal(True)
        self.progressDlg.show()
        self.worker.start()

    def suppliers_changed(self):
        for row in range(self.suppliersListWidget.count()):
            item = self.suppliersListWidget.item(row)
            shop = item.data(Qt.UserRole)
            for a in self.model.articles:
                if a.shopname == shop.name:
                    a.visible = item.checkState()
        self.model.refresh()


def run(shops=[Bike24(), BikeDiscount(), CNCBikes(), MTBNews()]):
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName("Bike Finder")
    QCoreApplication.setApplicationVersion("1.0.1")
    QCoreApplication.setOrganizationName("Stefan Lehmann")
    translator = QTranslator()
    tf = os.path.join(os.path.dirname(__file__), "articlefinder_de.qm")
    translator.load(tf)
    app.installTranslator(translator)
    w = MainWindow(shops)
    w.show()
    app.exec_()


if __name__ == "__main__":
    run()

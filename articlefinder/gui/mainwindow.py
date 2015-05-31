#! python3

import os
import sys
import webbrowser

from PyQt5.Qt import Qt
from PyQt5.QtCore import QTranslator, QCoreApplication, \
    QSettings, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from articlefinder.gui import preview

from articlefinder.gui.articlelist import ArticleListModel, PRICE, NAME, \
    ArticlelistWidget, ArticlelistDockWidget
from articlefinder.gui.preview import PreviewDockWidget, PreviewWidget
from articlefinder.gui.progressdialog import ProgressDialog
from articlefinder.gui.shoplist import ShoplistDockWidget

WINDOW_STATE_SETTING = "WindowState"
WINDOW_GEOMETRY_SETTING = "WindowGeometry"
HORIZONTAL_HEADER_SETTING = "HorizontalHeader"
VERTICAL_HEADER_SETTING = "VerticalHeader"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Central Widget with Result Table
        self.model = ArticleListModel()
        # self.articlelistDockWidget = ArticlelistDockWidget(self)
        self.articlelistWidget = ArticlelistWidget()
        # self.addDockWidget(Qt.BottomDockWidgetArea, self.articlelistDockWidget)
        self.setCentralWidget(self.articlelistWidget)
        self.table = self.articlelistWidget.resultTable
        self.table.setModel(self.model)
        self.model.table = self.articlelistWidget.resultTable

        # Signals
        self.articlelistWidget.searchLineEdit.returnPressed.connect(self.search)
        self.articlelistWidget.resultTable.clicked.connect(self.open_url)
        self.articlelistWidget.searchButton.pressed.connect(self.search)
        self.articlelistWidget.resultTable.mouseMoveEvent = self.resultTable_mouseMove

        # Supplier list
        self.shoplistDockWidget = ShoplistDockWidget(self)
        self.shoplistWidget = self.shoplistDockWidget.widget()
        self.shoplistWidget.checked_changed.connect(
            self.filter_checked_suppliers)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.shoplistDockWidget, Qt.Horizontal)

        # Preview
        self.previewDockWidget = PreviewDockWidget(self)
        self.previewWidget = self.previewDockWidget.widget()
        # self.setCentralWidget(self.previewWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.previewDockWidget,
                           Qt.Horizontal)

        # Articlelist


        self._init_menus()
        self.load_settings()

    def _init_menus(self):
        self.viewMenu = self.menuBar().addMenu(self.tr('View'))
        self.viewMenu.addAction(self.shoplistDockWidget.toggleViewAction())
        self.viewMenu.addAction(self.previewDockWidget.toggleViewAction())

    def closeEvent(self, event):
        self.save_settings()
        self.shoplistDockWidget.closeEvent(event)
        super().closeEvent(event)

    def filter_checked_suppliers(self):
        checked_shops = [shop.name for shop in
                         self.shoplistWidget.get_selected_shops()]

        for article in self.model.articles:
            article.visible = article.shop.name in checked_shops

        self.model.refresh()

    def load_settings(self):
        try:
            self.restoreState(QSettings().value(WINDOW_STATE_SETTING))
            self.restoreGeometry(QSettings().value(WINDOW_GEOMETRY_SETTING))
            self.table.horizontalHeader().restoreState(
                QSettings().value(HORIZONTAL_HEADER_SETTING)
            )
            self.table.verticalHeader().restoreState(
                QSettings().value(VERTICAL_HEADER_SETTING)
            )
        except (AttributeError, TypeError):
            self.resize(600, 800)

    def open_url(self, event):
        index = self.articlelistWidget.resultTable.currentIndex()
        if index.isValid():
            if index.column() == NAME:
                article = self.model.visible_articles[index.row()]
                # webbrowser.open_new_tab(article.url)
                self.previewWidget.load(QUrl(article.url))

    def progress(self, i, max, shopname):
        self.progressDlg.setMaximum(max)
        self.progressDlg.setLabelText(shopname)
        self.progressDlg.setValue(i)

    def resultTable_mouseMove(self, event):
        index = self.articlelistWidget.resultTable.indexAt(event.pos())
        if not index.isValid():
            self.articlelistWidget.resultTable.unsetCursor()

        if index.column() == NAME:
            self.articlelistWidget.resultTable.setCursor(Qt.PointingHandCursor)
        else:
            self.articlelistWidget.resultTable.unsetCursor()

    def save_settings(self):
        QSettings().setValue(WINDOW_STATE_SETTING, self.saveState())
        QSettings().setValue(WINDOW_GEOMETRY_SETTING, self.saveGeometry())
        QSettings().setValue(
            HORIZONTAL_HEADER_SETTING,
            self.table.horizontalHeader().saveState()
        )
        QSettings().setValue(
            VERTICAL_HEADER_SETTING,
            self.table.verticalHeader().saveState()
        )

    def search(self):

        def _get_suppliers():
            for row in range(self.shoplistWidget.count()):
                item = self.shoplistWidget.item(row)
                if item.checkState() == Qt.Checked:
                    yield item.data(Qt.UserRole)

        progressDlg = ProgressDialog(self)
        progressDlg.shops = self.shoplistWidget.get_selected_shops()
        progressDlg.run_search(self.articlelistWidget.searchLineEdit.text())
        progressDlg.exec_()

        self.model.beginResetModel()
        self.model.articles = progressDlg.articles
        self.model.refresh()
        self.model.endResetModel()
        self.articlelistWidget.resultTable.sortByColumn(PRICE, Qt.AscendingOrder)

    def suppliers_changed(self):
        for row in range(self.shoplistWidget.count()):
            item = self.shoplistWidget.item(row)
            shop = item.data(Qt.UserRole)
            for a in self.model.articles:
                if a.shopname == shop.name:
                    a.visible = item.checkState()
        self.model.refresh()


def run():
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName("Articlefinder")
    QCoreApplication.setApplicationVersion("1.0.1")
    QCoreApplication.setOrganizationName("Stefan Lehmann")
    translator = QTranslator()
    tf = os.path.join(os.path.dirname(__file__), "articlefinder_de.qm")
    translator.load(tf)
    app.installTranslator(translator)
    w = MainWindow()
    w.setWindowTitle("Articlefinder")
    w.show()
    app.exec_()


if __name__ == "__main__":
    run()

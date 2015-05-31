from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget, QApplication, QDockWidget
import sys


class PreviewWidget(QWebView):
    def __init__(self, parent=None):
        super().__init__(parent)


class PreviewDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PreviewDockWidget")
        self.setWindowTitle(self.tr("Preview"))
        self.setWidget(PreviewWidget())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PreviewWidget()
    w.load(QUrl("http://google.de"))
    w.show()
    app.exec_()

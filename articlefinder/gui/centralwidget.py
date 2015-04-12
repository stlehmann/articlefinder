from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QTableView, \
    QGridLayout, QApplication
import sys

__author__ = 'Lehmann'


class MyTableView(QTableView):
    pass


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
        self.resultTable = MyTableView()
        self.resultTable.setSortingEnabled(True)
        self.resultTable.setMouseTracking(True)
        self.resultTable.verticalHeader().sectionResized.connect(
            self.row_resized)

        #Layout
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.searchLabel, 0, 0)
        self.layout().addWidget(self.searchLineEdit, 0, 1)
        self.layout().addWidget(self.searchButton, 0, 2)
        self.layout().addWidget(self.resultTable, 1, 0, 1, 3)

    def row_resized(self, index, old_size, new_size):
        for i in range(self.resultTable.verticalHeader().count()):
            self.resultTable.setRowHeight(i, new_size)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CentralWidget()
    w.show()
    app.exec_()
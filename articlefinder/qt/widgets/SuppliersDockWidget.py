from PyQt5.QtWidgets import QDockWidget, QListWidget

__author__ = 'Lehmann'

class SuppliersDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(SuppliersDockWidget, self).__init__(parent)
        self.setObjectName("SuppliersDockWidget")
        self.setWindowTitle(self.tr("Supplier list"))
        self.suppliersListWidget = QListWidget()
        self.setWidget(self.suppliersListWidget)
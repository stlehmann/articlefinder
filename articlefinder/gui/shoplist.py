"""
Supply a List of all available Shops.

"""
import logging
import articlefinder.core.logger
import bisect
import importlib
import pkgutil
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt5.QtWidgets import QDockWidget, QListWidget, QWidget, QTreeView, \
    QVBoxLayout, QApplication
import sys


KEY, NODE = range(2)
logger = logging.getLogger('articlefinder.gui.shoplist')


def get_modules(pkg_name):
    package = importlib.import_module(pkg_name)
    prefix = package.__name__ + "."
    for path, module, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        yield module

class ModuleItem():
    def __init__(self, modulename):
        self.name = modulename

class Node():
    def __init__(self, parent=None):
        self.children = []
        self.item = ''
        self.parent = None

    def __len__(self):
        return len(self.children)

    def child_at_row(self, row: int):
        if 0 <= row < len(self.children):
            return self.children[row][NODE]
        return None

    def row_of_child(self, child):
        for i, item in enumerate(self.children):
            if item[NODE] == child:
                return i
        return -1

    def child_with_key(self, key):
        if not self.children:
            return
        i = bisect.bisect_left(self.children(key, None))
        if i < 0 or i >= len(self.children):
            return
        if self.children[i][KEY] == key:
            return self.children[i][NODE]

    def insert_child(self, child):
        child.parent = self
        bisect.insort(self.children, (child.order_key(), child))

    def order_key(self):
        return self.item.lower()

class Leaf():
    def __init__(self, item, parent=None):
        self.parent = parent
        self.item = item

    def __len__(self):
        return 0

    def order_key(self):
        if self.item is None:
            return ""
        return self.item


class ShoplistModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.root = self.init_root()

    def init_root(self):
        mainmodule = 'articlefinder.shops'
        def nodes_from_modules(parent):
            for module in get_modules(parent):
                try:
                    children = list(nodes_from_modules(module))
                except AttributeError as e:
                    logger.error(e)
                    children = []

                if children:
                    node = Node()
                    node.item = module
                    for child in children:
                        node.insert_child(child)
                    yield node
                else:
                    leaf = Leaf(module)
                    yield leaf

        root = Node()
        for child in nodes_from_modules(mainmodule):
            root.insert_child(child)
        return root

    def index(self, row: int, column: int, parent: QModelIndex()):
        assert self.root
        parent_node = self.node_from_index(parent)
        assert parent_node is not None
        return self.createIndex(row, column, parent_node.child_at_row(row))

    def parent(self, index=QModelIndex()):
        node = self.node_from_index(index)
        if node is None:
            return QModelIndex()
        parent = node.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.row_of_child(parent)
        assert row != -1
        return self.createIndex(row, 0, parent)

    def rowCount(self, parent=QModelIndex()):
        node = self.node_from_index(parent)
        return len(node)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return
        node = self.node_from_index(index)
        item = node.item
        if role == Qt.DisplayRole:
            if index.column() == 0:
                name = item.split('.')[-1]
                return name

    def node_from_index(self, index):
        return index.internalPointer() if index.isValid() else self.root


class ShoplistWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Treeview
        self.treeview = QTreeView()
        self.model = ShoplistModel()
        self.treeview.setModel(self.model)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.treeview)
        self.setLayout(layout)


class ShoplistDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(ShoplistDockWidget, self).__init__(parent)
        self.setObjectName("SuppliersDockWidget")
        self.setWindowTitle(self.tr("Supplier list"))
        self.setWidget(ShoplistWidget())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ShoplistWidget()
    w.show()
    app.exec_()
"""
Supply a List of all available Shops.

"""
import logging
import bisect
import importlib
import pkgutil
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt5.QtWidgets import QDockWidget, QListWidget, QWidget, QTreeView, \
    QVBoxLayout, QApplication, QPushButton
import sys


KEY, NODE = range(2)
logger = logging.getLogger('articlefinder.gui.shoplist')


def get_modules(pkg_name):
    package = importlib.import_module(pkg_name)
    prefix = package.__name__ + "."
    if hasattr(package, '__path__'):
        for path, modulename, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            yield modulename


class ModuleItem():
    def __init__(self, modulename):
        self.name = modulename


class Node():
    def __init__(self, parent=None):
        self.children = []
        self.item = ''
        self.parent = None
        self.checked = False

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
        return self.item.__name__.lower()


class Leaf():
    def __init__(self, item, parent=None):
        self.parent = parent
        self.item = item
        self.checked = False

    def __len__(self):
        return 0

    def order_key(self):
        return self.item.__name__.lower()


class ShoplistModel(QAbstractItemModel):
    columns = ["shop"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.root = self.init_root()

    def init_root(self):
        def nodes_from_modules(parent):
            for module in get_modules(parent):
                children = list(nodes_from_modules(module))

                if children:
                    node = Node()
                    node.item = importlib.import_module(module)
                    for child in children:
                        node.insert_child(child)
                    yield node
                else:
                    leaf = Leaf(importlib.import_module(module))
                    yield leaf

        root = Node()
        mainmodule = 'articlefinder.shops'
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
                if hasattr(item, "name"):
                    return item.name
                else:
                    name = item.__name__.split('.')[-1]
                    return name
        elif role == Qt.CheckStateRole:
            return Qt.Checked if node.checked else Qt.Unchecked

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if not index.isValid():
            return 0

        node = self.node_from_index(index)
        item = node.item

        if role == Qt.CheckStateRole:
            node.checked = value
            # if it is a node select the children
            if isinstance(node, Node):
                for key, child in node.children:
                    child.checked = value
                index0 = self.index(0, 0, index)
                index1 = self.index(len(node.children), 0, index)
                self.dataChanged.emit(index0, index1, [Qt.CheckStateRole])
            elif isinstance(node, Leaf):
                b = True
                for key, child in node.parent.children:
                    if not child.checked:
                        b = False; break
                node.parent.checked = b
                self.dataChanged.emit(index.parent(), index.parent(),
                    [Qt.CheckStateRole])
            self.dataChanged.emit(index, index)



            return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columns[section]

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 0:
            flags |= Qt.ItemIsUserCheckable
        return flags

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

    def get_shops(self):
        """
        List all shops.

        """
        def _iterate_items(parent):
            """
            Iterate over all shops and yield them.

            """
            for key, child in parent.children:
                if isinstance(child, Leaf):
                    yield child.item.create_shop()
                elif isinstance(child, Node):
                    for child in _iterate_items(child):
                        yield child

        root = self.model.root
        return list(_iterate_items(root))

    def get_selected_shops(self):
        """
        Get all shops that are selected.

        """
        def _find_selected_items(parent):
            """
            Iterate over all shops and yield the selected ones.

            """
            for key, child in parent.children:
                if isinstance(child, Leaf) and child.checked:
                    yield child.item.create_shop()
                elif isinstance(child, Node):
                    for child in _find_selected_items(child):
                        yield child

        root = self.model.root
        return list(_find_selected_items(root))


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
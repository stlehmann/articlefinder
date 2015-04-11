from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction


def create_action(parent, title, slot, shortcut=None, image=None, tip=""):
    action = QAction(title, parent)
    action.triggered.connect(slot)
    action.setStatusTip(tip)
    if shortcut is not None:
        action.setShortcut(shortcut)
    if image is not None:
        action.setIcon(QIcon(image))
    return action

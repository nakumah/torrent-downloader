from PySide6.QtWidgets import QWidget, QGridLayout
from qframelesswindow import FramelessMainWindow

from resources.styling import loadStyle
from views.components.nav_panel import NavPanel
from views.components.nav_stack import NavStack
from views.components.titlebar import CustomTitleBar


class MainWindow(FramelessMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.customTitleBar = CustomTitleBar(self)
        self.setTitleBar(self.customTitleBar)

        self.navPanel = NavPanel(self)
        self.navStack = NavStack(self)

        centralLayout = QGridLayout()
        centralLayout.addWidget(self.navPanel, 0, 0)
        centralLayout.addWidget(self.navStack, 0, 1)

        centralLayout.setContentsMargins(0, 0, 0, 0)
        centralLayout.setSpacing(0)
        centralLayout.setColumnStretch(1, 2)

        centralWidget = QWidget()
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

        self.setObjectName("MainWindow")
        self.setStyleSheet(loadStyle(":/qss/common.qss"))
        # self.setWindowIcon(QIcon(":/icons/icon.png"))

        self.titleBar.raise_()
        self.resize(700, 700)

    def setWindowIcon(self, icon, /):
        self.customTitleBar.setIcon(icon)
        return super().setWindowIcon(icon)

    def setWindowTitle(self, title, /):
        self.customTitleBar.setTitle(title)
        return super().setWindowTitle(title)

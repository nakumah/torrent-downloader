from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QPixmap
from qframelesswindow import TitleBar

from resources.styling import loadStyle
from views.components.search_input import SearchInput


class CustomTitleBar(TitleBar):


    def __init__(self, parent):
        super().__init__(parent=parent)

        self.searchInput = SearchInput()
        self.__titleLabel = QLabel(self)
        self.__labelButton = QPushButton(self)
        self.__labelButton.setFlat(True)

        centerWidgetLayout = QHBoxLayout()
        centerWidgetLayout.setContentsMargins(0,0,0,0)

        centerWidgetLayout.addWidget(self.searchInput)

        searchBar = QWidget()
        searchBar.setLayout(centerWidgetLayout)

        self.hBoxLayout.insertWidget(0, self.__labelButton)
        self.hBoxLayout.insertWidget(1, self.__titleLabel)
        self.hBoxLayout.insertStretch(2, 1)
        self.hBoxLayout.insertWidget(3, searchBar)
        self.hBoxLayout.setStretch(3, 2)

        self.setFixedHeight(50)

        self.setStyleSheet(loadStyle(":/qss/titlebar.qss"))


    def setIcon(self, icon: QIcon | QPixmap):
        self.__labelButton.setIcon(icon)

    def setTitle(self, title: str):
        self.__titleLabel.setText(title)
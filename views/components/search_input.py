from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QAction

import qtawesome

from resources.app_colors import appColors


class SearchInput(QLineEdit):

    searchReady = Signal(str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.searchAction = QAction(self)
        self.searchAction.setIcon(qtawesome.icon("msc.search", color=appColors.medium_rgb))

        self.clearSearchAction = QAction(self)
        self.clearSearchAction.setVisible(False)
        self.clearSearchAction.setIcon(qtawesome.icon("msc.close", color=appColors.medium_rgb))

        self.setPlaceholderText("Search Torrents ")
        self.addAction(self.searchAction, QLineEdit.ActionPosition.LeadingPosition)
        self.addAction(self.clearSearchAction, QLineEdit.ActionPosition.TrailingPosition)
        self.setObjectName("SearchInput")

        self.clearSearchAction.triggered.connect(self.__handleClearSearch)
        self.textEdited.connect(self.__handleSearchEdited)
        self.textChanged.connect(self.__handleTextChanged)
        self.editingFinished.connect(self.__handleEditingFinished)

        self.__buffer = ""
        self.__timer = QTimer()
        self.__timer.setSingleShot(True)
        self.__timer.setInterval(200) # 200 ms delay
        self.__timer.timeout.connect(self.__handleTimerElapsed)

    def __handleClearSearch(self):
        self.setText("")

    def __handleSearchEdited(self, text: str):
        self.__buffer = text

    def __handleEditingFinished(self):
        self.searchReady.emit(self.__buffer)

    def __handleTextChanged(self, text: str):

        self.clearSearchAction.setVisible(len(self.__buffer) > 0)

        self.__timer.stop()
        self.__buffer = text
        self.__timer.start() # restart the timer

    def __handleTimerElapsed(self):
        self.searchReady.emit(self.__buffer)

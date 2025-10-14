import typing

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc

from resources.app_colors import appColors
from resources.styling import loadStyle
from views.components.torrent_info_widget import TorrentInfoWidget
from views.components.torrents_table import BrowseTorrentsTable

import qtawesome as qta


class SearchPagePlaceholder(qtw.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = qtw.QVBoxLayout()

        title = qtw.QLabel()
        title.setObjectName("Title")
        title.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter)
        title.setText("Browse torrents online with searchbar")

        subTitle = qtw.QLabel()
        subTitle.setObjectName("Subtitle")
        subTitle.setAlignment(qtg.Qt.AlignmentFlag.AlignCenter)
        subTitle.setText("Data source: 1337")

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subTitle)
        layout.addStretch()

        self.setLayout(layout)
        self.setObjectName('SearchPagePlaceholder')


class PaginationToolBar(qtw.QFrame):
    triggered = qtc.Signal(int)  # The current. Invalid == 0

    def __init__(self, parent=None):
        super().__init__(parent)

        # region ui

        self.nextBtn = qtw.QToolButton()
        self.nextBtn.setIcon(qta.icon("fa5s.angle-right", color=appColors.dark_tint_rgb))
        self.nextBtn.setToolTip("Step Forward")

        self.prevBtn = qtw.QToolButton()
        self.prevBtn.setIcon(qta.icon("fa5s.angle-left", color=appColors.dark_tint_rgb))
        self.prevBtn.setToolTip("Step Backward")

        self.firstBtn = qtw.QToolButton()
        self.firstBtn.setIcon(qta.icon("fa5s.angle-double-left", color=appColors.dark_tint_rgb))
        self.firstBtn.setToolTip("First")

        self.lastBtn = qtw.QToolButton()
        self.lastBtn.setIcon(qta.icon("fa5s.angle-double-right", color=appColors.dark_tint_rgb))
        self.lastBtn.setToolTip("Last")

        self.currentPageInput = qtw.QLineEdit()
        self.currentPageInput.setMaximumWidth(50)
        self.currentPageInput.setAlignment(qtg.Qt.AlignmentFlag.AlignRight)
        self.totalPagesLabel = qtw.QLabel("-")

        toolbar = qtw.QToolBar()
        toolbar.addWidget(self.firstBtn)
        toolbar.addWidget(self.prevBtn)
        toolbar.addWidget(self.currentPageInput)
        toolbar.addWidget(qtw.QLabel("/"))
        toolbar.addWidget(self.totalPagesLabel)
        toolbar.addWidget(self.nextBtn)
        toolbar.addWidget(self.lastBtn)

        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(toolbar)
        layout.addStretch()

        self.setLayout(layout)
        self.setObjectName('PaginationToolBar')

        # region data
        self.__currentPage = 0
        self.__totalPages = 0

        self.__initialize()
        self.__configure()

    def __initialize(self):
        self.setTotalPages(0)
        self.setCurrentPage(0)

        self.enableButtons()
        return

    def __configure(self):
        self.nextBtn.clicked.connect(lambda: self.__handleBtnClicked("next"))
        self.prevBtn.clicked.connect(lambda: self.__handleBtnClicked("prev"))
        self.firstBtn.clicked.connect(lambda: self.__handleBtnClicked("first"))
        self.lastBtn.clicked.connect(lambda: self.__handleBtnClicked("last"))
        self.currentPageInput.editingFinished.connect(self.__handleCurrentPageInputTextEdited)

    # region getters

    def currentPage(self):
        return self.__currentPage

    def totalPages(self):
        return self.__totalPages

    # endregion

    # region setters

    def setCurrentPage(self, value: int):
        if value < 1:
            return
        self.__currentPage = value
        self.currentPageInput.setText(str(value))
        if value > self.__totalPages:
            self.setTotalPages(value)

        self.enableButtons()

    def setTotalPages(self, value: int):
        if value < 1:
            return

        self.__totalPages = value
        self.totalPagesLabel.setText(str(value))
        if value < self.__currentPage:
            self.__currentPage = 1
            self.currentPageInput.setText(str(1))

        self.enableButtons()

    # endregion

    # region event handlers

    def __handleCurrentPageInputTextEdited(self):
        text = self.currentPageInput.text()
        try:
            value = int(text)
        except ValueError:
            self.currentPageInput.setText(str(self.__currentPage))
            return

        if value == self.__currentPage:
            return

        if value < 1:
            self.currentPageInput.setText(str(self.__currentPage))

        if value > self.__totalPages:
            self.currentPageInput.setText(str(self.__currentPage))

        # update the buttons
        self.enableButtons()

        # dispatch the change
        self.triggered.emit(value)

    def __handleBtnClicked(self, btn: typing.Literal["next", "prev", "first", "last"]):
        if self.__totalPages == 0:
            return

        if btn == "next":
            page = self.__currentPage + 1
            if page == self.__totalPages:
                return
            self.__currentPage = page

        elif btn == "prev":
            page = self.__currentPage - 1
            if page < 1:
                return
            self.__currentPage = page
        elif btn == "first":
            self.__currentPage = 1
        elif btn == "last":
            self.__currentPage = self.__totalPages
        else:
            raise Exception("Invalid btn, expected 'next', 'prev', 'first', 'last', got {}".format(btn))

        self.enableButtons()
        self.currentPageInput.setText(str(self.__currentPage))
        self.triggered.emit(self.__currentPage)

    # endregion

    # region workers

    def __enableButton(self, btn: typing.Literal["next", "prev", "first", "last"], state: bool):
        if btn == "next":
            self.nextBtn.setEnabled(state)
        elif btn == "prev":
            self.prevBtn.setEnabled(state)
        elif btn == "first":
            self.firstBtn.setEnabled(state)
        elif btn == "last":
            self.lastBtn.setEnabled(state)
        else:
            raise Exception("Invalid btn, expected 'next', 'prev', 'first', 'last', got {}".format(btn))

    def enableButtons(self):
        if self.__totalPages == 0 or self.currentPageInput == 0:
            # disable all buttons
            for btn in ['next', 'prev', 'first', 'last', ]:
                self.__enableButton(btn, False)  # type: ignore
            return

        # enable the edge buttons
        if self.__totalPages > 0:
            self.__enableButton("first", True)
            self.__enableButton("last", True)

        # en/disable target buttons
        if self.__currentPage == 1:
            self.__enableButton("next", True)
            self.__enableButton("prev", False)
        elif self.__currentPage == self.__totalPages:
            self.__enableButton("next", False)
            self.__enableButton("prev", True)
        else:
            self.__enableButton("next", True)
            self.__enableButton("prev", True)

    # endregion


class SearchPage(qtw.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        pageTitle = qtw.QLabel("Search Online")
        pageTitle.setObjectName('PageTitle')
        pageTitle.hide()

        pagePlaceholder = SearchPagePlaceholder()

        self.progressBar = qtw.QProgressBar(self)
        self.progressBar.setFixedHeight(5)
        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0, 0)

        self.categoryComboBox = qtw.QComboBox()
        self.categoryComboBox.setPlaceholderText('Search Category ...')

        self.sortByComboBox = qtw.QComboBox()
        self.sortByComboBox.setPlaceholderText("Sort by ...")

        self.paginationToolbar = PaginationToolBar()
        self.torrentsTable = BrowseTorrentsTable()

        headerLayout = qtw.QHBoxLayout()
        headerLayout.setContentsMargins(0, 0, 0, 0)
        headerLayout.addWidget(self.paginationToolbar)
        headerLayout.addStretch()
        headerLayout.addWidget(qtw.QLabel('Category:'))
        headerLayout.addWidget(self.categoryComboBox)
        headerLayout.addWidget(self.sortByComboBox)

        self.header = qtw.QFrame(self)
        self.header.setLayout(headerLayout)

        self.contentStack = qtw.QStackedWidget()
        self.contentStack.addWidget(pagePlaceholder)
        self.contentStack.addWidget(self.torrentsTable)
        self.contentStack.setCurrentIndex(1)

        topLayout = qtw.QVBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.addWidget(self.contentStack)

        topWidget = qtw.QWidget()
        topWidget.setLayout(topLayout)

        self.torrentInfoWidget = TorrentInfoWidget()

        bottomLayout = qtw.QVBoxLayout()
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        bottomLayout.addWidget(self.torrentInfoWidget)

        self.bottomWidget = qtw.QWidget()
        self.bottomWidget.setLayout(bottomLayout)

        pageSplitter = qtw.QSplitter(qtg.Qt.Orientation.Vertical)
        pageSplitter.addWidget(topWidget)
        pageSplitter.addWidget(self.bottomWidget)
        pageSplitter.setChildrenCollapsible(False)

        pageLayout = qtw.QGridLayout()
        pageLayout.setContentsMargins(20, 0, 20, 10)

        pageLayout.addWidget(self.progressBar)
        pageLayout.addWidget(pageTitle)
        pageLayout.addWidget(self.header)
        pageLayout.addWidget(pageSplitter)
        pageLayout.setRowStretch(3, 1)

        self.setLayout(pageLayout)

        self.setObjectName("SearchPage")
        self.setStyleSheet(loadStyle(":/qss/search_page.qss"))
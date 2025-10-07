import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from resources.styling import loadStyle
from views.components.torrents_table import BrowseTorrentsTable


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


class SearchPage(qtw.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        pageTitle = qtw.QLabel("Search Online")
        pageTitle.setObjectName('PageTitle')
        pageTitle.hide()

        pagePlaceholder = SearchPagePlaceholder()
        self.torrentsTable = BrowseTorrentsTable()

        self.contentStack = qtw.QStackedWidget()
        self.contentStack.addWidget(pagePlaceholder)
        self.contentStack.addWidget(self.torrentsTable)
        self.contentStack.setCurrentIndex(1)

        pageLayout = qtw.QGridLayout()
        pageLayout.setContentsMargins(20, 30, 20, 10)

        pageLayout.addWidget(pageTitle)
        pageLayout.addWidget(self.contentStack)
        pageLayout.setRowStretch(1, 1)

        self.setLayout(pageLayout)

        self.setObjectName("SearchPage")
        self.setStyleSheet(loadStyle(":/qss/search_page.qss"))
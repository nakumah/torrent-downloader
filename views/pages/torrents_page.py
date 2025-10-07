import PySide6.QtWidgets as qtw

from resources.styling import loadStyle
from views.components.check_badges import CheckBadgeGroup
from views.components.torrents_table import ActiveTorrentsTable


class TorrentsPage(qtw.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)


        pageTitle = qtw.QLabel("Torrents")
        pageTitle.setObjectName('PageTitle')

        self.filterGroup = CheckBadgeGroup()
        self.filterGroup.addBadge("All", "all")
        self.filterGroup.addBadge("Completed", "completed")
        self.filterGroup.addBadge("Uploading", "uploading")
        self.filterGroup.addBadge("Downloading", "downloading")

        self.torrentsTable = ActiveTorrentsTable()

        pageLayout = qtw.QGridLayout()
        pageLayout.setContentsMargins(20, 30, 20, 10)

        pageLayout.addWidget(pageTitle)
        pageLayout.addWidget(self.filterGroup)
        pageLayout.addWidget(self.torrentsTable)

        pageLayout.setRowStretch(2, 1)
        pageLayout.setVerticalSpacing(10)

        self.setLayout(pageLayout)

        self.setObjectName("TorrentsPage")
        self.setStyleSheet(loadStyle(":/qss/torrents_page.qss"))


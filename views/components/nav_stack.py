from PySide6.QtWidgets import QFrame, QStackedWidget, QVBoxLayout

from core.structures import NavPages
from resources.styling import loadStyle
from views.pages.dashboard_page import DashboardPage
from views.pages.search_page import SearchPage
from views.pages.settings_page import SettingsPage
from views.pages.torrents_page import TorrentsPage


class NavStack(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__pages: dict[NavPages, DashboardPage] = {
            NavPages.DASHBOARD: DashboardPage(),
            NavPages.TORRENTS: TorrentsPage(),
            NavPages.SEARCH: SearchPage(),
            NavPages.SETTINGS: SettingsPage(),
        }
        self.__idxMap: dict[NavPages, int] = {}

        self.contentWidget = QStackedWidget(self)
        for k, page in self.__pages.items():
            idx = self.contentWidget.addWidget(page)
            self.__idxMap[k] = idx

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.contentWidget)

        self.setLayout(layout)
        self.setMinimumHeight(300)

        self.setObjectName("NavStack")
        self.setStyleSheet(loadStyle(":/qss/nav_stack.qss"))

    def setCurrentPage(self, page: NavPages):
        stackId = self.__idxMap.get(page, None)
        if stackId is None:
            return
        self.contentWidget.setCurrentIndex(stackId)
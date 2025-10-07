from PySide6.QtWidgets import QFrame, QStackedWidget, QVBoxLayout

from resources.styling import loadStyle
from views.pages.dashboard_page import DashboardPage
from views.pages.torrents_page import TorrentsPage


class NavStack(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__pages: dict[str, DashboardPage] = {
            "dashboard": DashboardPage(),
            "torrents": TorrentsPage(),
        }
        self.__idxMap: dict[int, str] = {}

        self.contentWidget = QStackedWidget(self)
        for k, page in self.__pages.items():
            idx = self.contentWidget.addWidget(page)
            self.__idxMap[idx] = k
            self.contentWidget.setCurrentIndex(idx)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.contentWidget)

        self.setLayout(layout)
        self.setMinimumHeight(300)

        self.setObjectName("NavStack")
        self.setStyleSheet(loadStyle(":/qss/nav_stack.qss"))

from PySide6.QtWidgets import QFrame, QStackedLayout, QLabel, QStackedWidget, QVBoxLayout, QWidget

from resources.styling import loadStyle
from views.pages.dashboard_page import DashboardPage


class NavStack(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__pages: dict[str, DashboardPage] = {
            "dashboard": DashboardPage(),
        }
        self.__idxMap: dict[int, str] = {}

        self.contentWidget = QStackedWidget(self)
        for k, page in self.__pages.items():
            idx = self.contentWidget.addWidget(page)
            self.__idxMap[idx] = k

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.contentWidget)

        self.setLayout(layout)
        self.setMinimumHeight(300)

        self.setObjectName("NavStack")
        self.setStyleSheet(loadStyle(":/qss/nav_stack.qss"))

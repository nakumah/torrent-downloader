import qtawesome
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QToolButton, QWidget, QToolBar, QGridLayout, QSizePolicy

from resources.app_colors import appColors
from resources.styling import loadStyle


class NavPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.dashboardBtn = QToolButton(self)
        self.dashboardBtn.setText("DASHBOARD")
        self.dashboardBtn.setIcon(qtawesome.icon("msc.home", color=appColors.medium_rgb, color_active=appColors.primary_rgb))
        self.dashboardBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.dashboardBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.dashboardBtn.setObjectName("NavPanelButton")

        self.torrensBtn = QToolButton(self)
        self.torrensBtn.setText("TORRENTS")
        self.torrensBtn.setIcon(qtawesome.icon("msc.rocket", color=appColors.medium_rgb, color_active=appColors.primary_rgb))
        self.torrensBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.torrensBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.torrensBtn.setObjectName("NavPanelButton")

        self.searchBtn = QToolButton(self)
        self.searchBtn.setText("SEARCH")
        self.searchBtn.setIcon(qtawesome.icon("msc.search", color=appColors.medium_rgb, color_active=appColors.primary_rgb))
        self.searchBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.searchBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.searchBtn.setObjectName("NavPanelButton")

        self.settings = QToolButton(self)
        self.settings.setText("SETTINGS")
        self.settings.setIcon(qtawesome.icon("msc.settings-gear", color=appColors.medium_rgb, color_active=appColors.primary_rgb))
        self.settings.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.settings.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.settings.setObjectName("NavPanelButton")

        toolbar = QToolBar(self)
        toolbar.setOrientation(Qt.Orientation.Vertical)
        toolbar.addWidget(self.dashboardBtn)
        toolbar.addWidget(self.torrensBtn)
        toolbar.addWidget(self.searchBtn)
        toolbar.addWidget(self.settings)

        layout = QGridLayout()
        layout.addWidget(QWidget())
        layout.addWidget(toolbar)
        layout.addWidget(QWidget())

        layout.setRowStretch(0, 1)
        layout.setRowStretch(2, 1)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.setObjectName("NavPanel")
        self.setStyleSheet(loadStyle(":/qss/nav_panel.qss"))
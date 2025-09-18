import numpy as np
import qtawesome
from PySide6.QtCharts import QChart, QChartView, QSplineSeries, QAreaSeries
from PySide6.QtCore import QSize
from PySide6.QtGui import (QBrush, QIcon)
from PySide6.QtWidgets import (QFrame, QLabel, QWidget, QPushButton, QTableView,
                               QGridLayout, QVBoxLayout, QToolButton)

from resources.app_colors import appColors
from resources.styling import loadStyle, parseStyle


class DashboardGraph(QFrame):
    def __init__(self):
        super().__init__()

        self.downloadSeries = QAreaSeries(color=appColors.success_tint_rgb, borderColor=appColors.success_shade_rgb)
        self.downloadSeries.setName("Bytes Downloaded")

        self.uploadSeries = QAreaSeries(color=appColors.secondary_tint_rgb, borderColor=appColors.secondary_shade_rgb)
        self.uploadSeries.setName("Bytes Uploaded")

        self.chart = QChart()
        self.chart.addSeries(self.downloadSeries)
        self.chart.addSeries(self.uploadSeries)

        self.chartView = QChartView(self.chart)
        self.chartView.setBackgroundBrush(QBrush(appColors.light_rgb))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chartView)

        self.setLayout(layout)

        self.setObjectName("DashboardGraph")

        self.__plots = {}

        self.populate()

    def populate(self):

        x = np.linspace(0, np.pi, 500)
        y0 = np.zeros_like(x)
        y1 = np.cos(x)
        y2 = np.sin(x)

        # lower series
        ls1 = QSplineSeries()
        ls2 = QSplineSeries()
        us1 = QSplineSeries()
        us2 = QSplineSeries()

        for i in range(x.shape[0]):
            ls1.append(float(x[i]), float(y0[i]))
            us1.append(float(x[i]), float(y1[i]))

            ls2.append(float(x[i]), float(y0[i]))
            us2.append(float(x[i]), float(y2[i]))

        self.downloadSeries.setLowerSeries(ls1)
        self.downloadSeries.setUpperSeries(us1)

        self.uploadSeries.setLowerSeries(ls2)
        self.uploadSeries.setUpperSeries(us2)

        self.chart.createDefaultAxes()


class DashboardTile(QFrame):
    def __init__(self, icon: QIcon, bgColor: str, title: str = "", subtitle: str = "", parent=None):
        super().__init__(parent)

        self.primaryTitle = QLabel(title)
        self.primaryTitle.setObjectName('DashboardTilePrimaryTitle')

        self.secondaryTitle = QLabel(subtitle)
        self.secondaryTitle.setObjectName('DashboardTileSecondaryTitle')

        badge = QToolButton()
        badge.setIcon(icon)
        badge.setIconSize(QSize(32, 32))
        badge.setFixedSize(50, 50)
        badge.setObjectName("DashboardTileBadge")

        padding = QWidget()
        padding.setMinimumHeight(20)

        layout = QGridLayout()
        layout.addWidget(badge, 0, 0)
        layout.addWidget(padding, 1, 0)
        layout.addWidget(self.primaryTitle, 2, 0, 1, 2)
        layout.addWidget(self.secondaryTitle, 3, 0, 1, 2)

        self.setLayout(layout)

        self.setFixedWidth(150)

        self.setObjectName("DashboardTile")
        self.setStyleSheet(parseStyle(
            """
                QFrame#DashboardTile{
                    border-radius: 20px;
                    border: 1px solid %s;
                    background-color: %s;
                }
            """.replace("%s", bgColor)
        ))


class DashboardPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        pageTitle = QLabel("Dashboard")
        pageTitle.setObjectName('PageTitle')

        tableLabel = QLabel("Recent torrents")
        tableLabel.setObjectName('TableLabel')

        self.overviewGraph = DashboardGraph()
        self.uploadedTile = DashboardTile(qtawesome.icon("msc.cloud-upload", color=appColors.light_rgb),
                                          appColors.highlight_rgb, "32.32 Gb", "Bytes Uploaded")
        self.downloadedTile = DashboardTile(qtawesome.icon("msc.cloud-download", color=appColors.light_rgb),
                                            appColors.secondary_tint_rgb, "21.90 GB", "Bytes downloaded")
        self.usedTile = DashboardTile(qtawesome.icon("msc.chip", color=appColors.dark_tint_rgb),
                                      appColors.hover_shade_rgb, "3.2 Gb", "Used of 20Gb")
        self.seeAllTorrentsBtn = QPushButton("SEE ALL TORRENTS")
        self.seeAllTorrentsBtn.setObjectName("SeeAllTorrentsBtn")
        self.recentTorrentsTable = QTableView()

        tileLayout = QGridLayout()
        tileLayout.addWidget(self.overviewGraph, 0, 0, 2, 1)
        tileLayout.addWidget(self.uploadedTile, 0, 1)
        tileLayout.addWidget(self.downloadedTile, 0, 2)
        tileLayout.addWidget(self.usedTile, 1, 1)
        tileLayout.setColumnStretch(0, 1)

        tileHolder = QFrame()
        tileHolder.setLayout(tileLayout)
        tileHolder.setObjectName('TileHolder')

        pageLayout = QGridLayout()
        pageLayout.setContentsMargins(20, 30, 20, 10)

        paddWidget = QWidget()
        paddWidget.setFixedHeight(25)

        pageLayout.addWidget(pageTitle, 0, 0)
        pageLayout.addWidget(tileHolder, 1, 0, 1, 4)
        pageLayout.addWidget(paddWidget, 2, 0)
        pageLayout.addWidget(tableLabel, 3, 0)
        pageLayout.addWidget(self.seeAllTorrentsBtn, 3, 3)
        pageLayout.addWidget(self.recentTorrentsTable, 4, 0, 1, 4)

        pageLayout.setColumnStretch(1, 2)

        self.setLayout(pageLayout)

        self.setObjectName("DashboardPage")
        self.setStyleSheet(loadStyle(":/qss/dashboard.qss"))

from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem

from core.structures import TorrentCategory, BrowseTableColumns
from core.workers import getIconFromCategory
from views.components.cell_widgets import TorrentActivityWidget, TorrentActionToolButton, TorrentCellAction


class ActiveTorrentsTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        self.setColumnCount(3)
        self.setRowCount(0)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setObjectName("ActiveTorrentsTable")

    def __populate(self):
        self.setRowCount(3)

        exts = [TorrentCategory.MOVIES, TorrentCategory.TV, TorrentCategory.ANIME]

        for row in range(3):
            activityWidget = TorrentActivityWidget()
            icon = getIconFromCategory(exts[row])
            pix = icon.pixmap(24, 24)
            activityWidget.previewImageLabel.setPixmap(pix)

            infoButton = TorrentActionToolButton(cellAction=TorrentCellAction.INFO)
            if row == 0:
                actionButton = TorrentActionToolButton(cellAction=TorrentCellAction.RESUME)
            elif row == 1:
                actionButton = TorrentActionToolButton(cellAction=TorrentCellAction.STOP)
            else:
                actionButton = TorrentActionToolButton(cellAction=TorrentCellAction.PAUSE)

            self.setCellWidget(row, 0, activityWidget)
            self.setCellWidget(row, 1, infoButton)
            self.setCellWidget(row, 2, actionButton)


class BrowseTorrentsTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.verticalHeader().setVisible(False)

        self.setAlternatingRowColors(True)

        self.resetTable()
        self.setObjectName("BrowseTorrentsTable")

        self.__configure()

    def __configure(self):
        self.cellClicked.connect(lambda row, col: self.__highlightRow(row))

    def __highlightRow(self, row):
        selectionModel = self.selectionModel()
        flag = QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows
        selectionModel.select(self.model().index(row, 0), flag)

    def resetTable(self):
        self.clear()

        self.setColumnCount(6)
        self.setRowCount(0)

        # configure horizontal header
        nameHeaderItem = QTableWidgetItem("Name")
        nameHeaderItem.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setHorizontalHeaderItem(BrowseTableColumns.NAME, nameHeaderItem)

        columnNames = ["Name", "Seeders", "Leechers", "Time", "Size", "Uploader"]
        self.setHorizontalHeaderLabels(columnNames)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # configure vertical header
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    @staticmethod
    def __configureItem(col: int, item: QTableWidgetItem):
        if col == BrowseTableColumns.NAME:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        itemFlags = Qt.ItemFlag.ItemIsEnabled |  Qt.ItemFlag.ItemIsSelectable
        item.setFlags(itemFlags)

    def setItem(self, row, col, item):

        self.__configureItem(col, item)

        return super().setItem(row, col, item)

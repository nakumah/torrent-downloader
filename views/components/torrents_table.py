from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from views.components.cell_widgets import TorrentActivityWidget, TorrentActionToolButton, TorrentCellAction


class TorrentsTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)


        self.setColumnCount(3)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.__populate()

        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def __populate(self):
        self.setRowCount(3)

        for row in range(3):
            activityWidget = TorrentActivityWidget()
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

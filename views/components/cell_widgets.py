from enum import IntEnum

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QToolButton, QGridLayout, QProgressBar
from PySide6.QtCore import Qt, QSize

from resources.app_colors import appColors

import qtawesome

class TorrentActivityWidget(QFrame):
    def __init__(self, parent: QFrame = None):
        super().__init__(parent=parent)

        downloadIconWidget = qtawesome.IconWidget("msc.cloud-download", color=appColors.medium_rgb)
        uploadIconWidget = qtawesome.IconWidget("msc.cloud-upload", color=appColors.medium_rgb)
        etaIconWidget = qtawesome.IconWidget("fa5s.clock", color=appColors.medium_rgb)

        self.torrentNameLabel = QLabel(self)
        self.uploadSpeedLabel = QLabel(self)
        self.downloadSpeedLabel = QLabel(self)
        self.percentageCompletedLabel = QLabel(self)
        self.etaLabel = QLabel(self)
        self.optionsButton = QToolButton(self)
        self.optionsButton.setIcon(qtawesome.icon("msc.kebab-vertical", color=appColors.medium_rgb))
        self.shareButton = QToolButton(self)
        self.shareButton.setIcon(qtawesome.icon("msc.share", color=appColors.medium_rgb))

        self.progressBar = QProgressBar(self)

        self.previewImageLabel = QLabel(self)
        self.previewImageLabel.setFixedSize(45, 45)

        layout = QGridLayout()

        layout.addWidget(self.previewImageLabel, 0, 0, 3, 1)

        layout.addWidget(self.torrentNameLabel, 0, 1, 1, 6)
        layout.addWidget(self.shareButton, 0, 8, 1, 1 )
        layout.addWidget(self.optionsButton, 0, 9, 1, 1 )
        layout.addWidget(QLabel(), 0, 7)

        layout.addWidget(downloadIconWidget, 1, 1)
        layout.addWidget(self.downloadSpeedLabel, 1, 2)
        layout.addWidget(uploadIconWidget, 1, 3)
        layout.addWidget(self.uploadSpeedLabel, 1, 4)
        layout.addWidget(etaIconWidget, 1, 5)
        layout.addWidget(self.etaLabel, 1, 6)
        layout.addWidget(self.percentageCompletedLabel, 1, 9)

        layout.addWidget(self.progressBar, 2, 1, 1, 9)

        layout.setColumnStretch(7, 1)

        self.setLayout(layout)

        self.setObjectName("TorrentActivityWidget")

        self.__populate()

    def __populate(self):
        self.torrentNameLabel.setText("Torrent Name: The last torrent bender.mp4")
        self.uploadSpeedLabel.setText("3.24 MB/s")
        self.downloadSpeedLabel.setText("3.24 MB/s")
        self.percentageCompletedLabel.setText("55.2 %")
        self.etaLabel.setText("2 mins 45 sec")

        self.progressBar.setRange(0, 100)
        self.progressBar.setTextVisible(False)
        self.progressBar.setValue(88)

        pix = QPixmap(":/images/logo.png").scaled(45, 45)
        self.previewImageLabel.setPixmap(pix)

class TorrentCellAction(IntEnum):
    INFO = 0
    RESUME = 1
    PAUSE = 2
    STOP = 3
    UNSET = -1


class TorrentActionToolButton(QToolButton):
    def __init__(self, cellAction: TorrentCellAction = TorrentCellAction.UNSET, **kwargs):
        super().__init__(**kwargs)

        self.__cellAction = TorrentCellAction.UNSET
        self.setCellAction(cellAction)
        self.setIconSize(QSize(30, 30))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setObjectName("TorrentActionToolButton")

    def __initialize(self):
        if self.__cellAction == TorrentCellAction.INFO:
            self.setIcon(qtawesome.icon("msc.info", color=appColors.primary_rgb))
            self.setToolTip("INFO")

        if self.__cellAction == TorrentCellAction.RESUME:
            self.setIcon(qtawesome.icon("msc.play-circle", color=appColors.success_rgb))
            self.setToolTip("RESUME")

        if self.__cellAction == TorrentCellAction.PAUSE:
            self.setIcon(qtawesome.icon("msc.debug-pause", color=appColors.medium_rgb))
            self.setToolTip("PAUSE")

        if self.__cellAction == TorrentCellAction.STOP:
            self.setIcon(qtawesome.icon("msc.stop-circle", color=appColors.danger_rgb))
            self.setToolTip("STOP")

        if self.__cellAction == TorrentCellAction.UNSET:
            self.setIcon(qtawesome.icon("msc.account", color=appColors.white_rgb))
            self.setToolTip("UNSET")

    def setCellAction(self, cellAction: TorrentCellAction):
        self.__cellAction = cellAction
        self.__initialize()

    def cellAction(self) -> TorrentCellAction:
        return self.__cellAction
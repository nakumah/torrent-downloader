import os

import PySide6.QtGui as qtg
import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
import qtawesome as qta
from py1337x.models import TorrentInfo

from resources.app_colors import appColors
from resources.styling import loadStyle
from views.components.common import QColoredLabel, QWeightedColorLabel


class TorrentPreviewDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        pix = qtg.QPixmap(":/images/torrent_file.png").scaled(64, 64)
        self.thumbnailLabel = qtw.QLabel(pixmap=pix)

        self.titleLabel = QWeightedColorLabel(color=appColors.dark_rgb,)
        self.totalSizeLabel = qtw.QLabel()
        self.seedersLabel = QColoredLabel(color=appColors.success_shade_rgb,)
        self.leechersLabel = QColoredLabel(color=appColors.danger_shade_rgb,)
        self.saveDirectoryInput = qtw.QLineEdit()
        self.browseDirectoryButton = qtw.QPushButton()
        self.browseDirectoryButton.setIcon(qta.icon("msc.ellipsis", color=appColors.dark_rgb))
        self.browseDirectoryButton.setFixedWidth(40)

        self.setWindowTitle("Torrent Preview")

        sectionOneLayout = qtw.QGridLayout()
        sectionOneLayout.addWidget(self.thumbnailLabel, 0, 0, 3, 1)
        sectionOneLayout.addWidget(self.titleLabel, 0, 1, 1, 4)
        sectionOneLayout.addWidget(QWeightedColorLabel(color=appColors.dark_rgb, text="Total Size:"), 1, 1)
        sectionOneLayout.addWidget(self.totalSizeLabel, 1, 2)
        sectionOneLayout.addWidget(QWeightedColorLabel(color=appColors.dark_rgb, text="Seeders:"), 2, 1)
        sectionOneLayout.addWidget(self.seedersLabel, 2, 2)
        sectionOneLayout.addWidget(QWeightedColorLabel(color=appColors.dark_rgb, text="Leechers:"), 2, 3)
        sectionOneLayout.addWidget(self.leechersLabel, 2, 4)
        sectionOneLayout.addWidget(qtw.QWidget(), 1, 5)
        sectionOneLayout.setColumnStretch(5, 1)

        sectionOneWidget = qtw.QFrame()
        sectionOneWidget.setContentsMargins(0, 0, 0, 0)
        sectionOneWidget.setObjectName("sectionOneWidget")
        sectionOneWidget.setLayout(sectionOneLayout)

        sectionTwoLayout = qtw.QGridLayout()
        sectionTwoLayout.addWidget(self.saveDirectoryInput, 0, 0)
        sectionTwoLayout.addWidget(self.browseDirectoryButton, 0, 1)

        sectionTwoWidget = qtw.QGroupBox("Save")
        sectionTwoWidget.setObjectName("saveGroupBox")
        sectionTwoWidget.setLayout(sectionTwoLayout)

        acceptButton = qtw.QPushButton("Begin Download")
        rejectButton = qtw.QPushButton("Cancel")

        # qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel,
        self.buttonBox = qtw.QDialogButtonBox()
        self.buttonBox.addButton(acceptButton, qtw.QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(rejectButton, qtw.QDialogButtonBox.ButtonRole.RejectRole)

        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(sectionOneWidget)
        layout.addWidget(sectionTwoWidget)
        layout.addStretch()
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.setObjectName("PreviewDialog")
        self.setStyleSheet(loadStyle(":/qss/preview_dialog.qss"))

        self.__configure()

    def __configure(self):

        self.browseDirectoryButton.clicked.connect(self.__handleBrowseBtnClicked)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def __clear__(self):
        self.titleLabel.setText("-")
        self.totalSizeLabel.setText("-")
        self.seedersLabel.setText("-")
        self.leechersLabel.setText("-")
        self.saveDirectoryInput.setText("-")


    def populate(self, model: TorrentInfo = None, saveDirectory: str = None):

        self.titleLabel.setText(f"{model.name}")
        self.totalSizeLabel.setText(f"{model.size}")
        self.seedersLabel.setText(f"{model.seeders}")
        self.leechersLabel.setText(f"{model.leechers}")
        self.saveDirectoryInput.setText(f"{saveDirectory}")

    def launch(self, model: TorrentInfo = None, saveDirectory: str = None):

        self.__clear__()
        self.populate(model, saveDirectory)
        return self.exec_()

    # region event handlers

    def __handleBrowseBtnClicked(self):
        folder = qtw.QFileDialog.getExistingDirectory(self, "Select a Folder")

        if not os.path.exists(folder):
            return

        self.saveDirectoryInput.setText(folder)
        return

    # endregion

    # region getters

    def saveFolder(self) -> str | None:
        """ return save folder if input is valid, else return None """
        text = self.saveDirectoryInput.text()
        if os.path.exists(text):
            return text
        else:
            return None

    # endregion
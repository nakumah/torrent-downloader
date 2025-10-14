import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import qtawesome

from resources.app_colors import appColors
from resources.styling import loadStyle
from views.components.common import QWeightedColorLabel, QColoredLabel


class TorrentInfoWidget(qtw.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thumbnailLabel = qtw.QLabel()
        pixmap = qtg.QPixmap(":/images/torrent_file.png").scaled(128, 128)
        self.thumbnailLabel.setPixmap(pixmap)

        self.thumbnailLabel.setObjectName("TorrentThumbnailLabel")

        self.nameValueLabel = qtw.QLabel(text="")
        self.nameValueLabel.setObjectName("TorrentNameValueLabel")

        self.categoryValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.typeValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.languageValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.totalSizeValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.uploadedByValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.downloadsValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.lastCheckedValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.dateUploadedValueLabel = QColoredLabel(color=appColors.medium_rgb)
        self.seedersValueLabel = QColoredLabel(color=appColors.success_shade_rgb)
        self.leechersValueLabel = QColoredLabel(color=appColors.danger_shade_rgb)

        categoryLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Category")
        typeLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Type")
        languageLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Language")
        totalSizeLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Total Size")
        uploadedByLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Uploaded By")
        downloadsLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Downloads")
        lastCheckedLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Last Checked")
        dateUploadedLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Date Uploaded")
        seedersLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Seeders")
        leechersLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="Leechers")

        self.magnetDownloadButton = qtw.QPushButton()
        self.magnetDownloadButton.setObjectName("MagnetDownloadButton")
        self.magnetDownloadButton.setToolTip("Download Via Magnet")
        self.magnetDownloadButton.setText("Magnet Download")
        self.magnetDownloadButton.setIcon(qtawesome.icon("msc.magnet", color=appColors.light_rgb))

        sectionOneLayout = qtw.QGridLayout()

        # other
        sectionOneLayout.addWidget(self.thumbnailLabel, 0, 0, 6, 1)
        sectionOneLayout.addWidget(self.nameValueLabel, 0, 1, 1, 4)

        # set 1
        sectionOneLayout.addWidget(categoryLabel, 1, 1)
        sectionOneLayout.addWidget(typeLabel, 2, 1)
        sectionOneLayout.addWidget(languageLabel, 3, 1)
        sectionOneLayout.addWidget(totalSizeLabel, 4, 1)
        sectionOneLayout.addWidget(uploadedByLabel, 5, 1)

        sectionOneLayout.addWidget(self.categoryValueLabel, 1, 2)
        sectionOneLayout.addWidget(self.typeValueLabel, 2, 2)
        sectionOneLayout.addWidget(self.languageValueLabel, 3, 2)
        sectionOneLayout.addWidget(self.totalSizeValueLabel, 4, 2)
        sectionOneLayout.addWidget(self.uploadedByValueLabel, 5, 2)

        # set 2
        sectionOneLayout.addWidget(downloadsLabel, 1, 3)
        sectionOneLayout.addWidget(lastCheckedLabel, 2, 3)
        sectionOneLayout.addWidget(dateUploadedLabel, 3, 3)
        sectionOneLayout.addWidget(seedersLabel, 4, 3)
        sectionOneLayout.addWidget(leechersLabel, 5, 3)

        sectionOneLayout.addWidget(self.downloadsValueLabel, 1, 4)
        sectionOneLayout.addWidget(self.lastCheckedValueLabel, 2, 4)
        sectionOneLayout.addWidget(self.dateUploadedValueLabel, 3, 4)
        sectionOneLayout.addWidget(self.seedersValueLabel, 4, 4)
        sectionOneLayout.addWidget(self.leechersValueLabel, 5, 4)

        # set 3
        sectionOneLayout.addWidget(qtw.QWidget(), 0, 5)
        sectionOneLayout.addWidget(self.magnetDownloadButton, 0, 6, 1, 1)
        sectionOneLayout.setColumnStretch(5, 1)
        sectionOneLayout.setHorizontalSpacing(20)
        sectionOneLayout.setVerticalSpacing(5)

        sectionOneWidget = qtw.QFrame()
        sectionOneWidget.setLayout(sectionOneLayout)

        #
        infoHashLabel = QWeightedColorLabel(color=appColors.dark_rgb, text="INFOHASH")
        self.infoHashValueLabel = QColoredLabel(color=appColors.dark_rgb, text="")
        self.copyInfoHashButton = qtw.QPushButton()
        self.copyInfoHashButton.setToolTip("Copy Info Hash")
        self.copyInfoHashButton.setIcon(qtawesome.icon("msc.copy", color=appColors.dark_tint_rgb))
        self.copyInfoHashButton.setFlat(True)

        sectionTwoLayout = qtw.QGridLayout()
        sectionTwoLayout.addWidget(infoHashLabel, 0, 0)
        sectionTwoLayout.addWidget(self.infoHashValueLabel, 0, 1)
        sectionTwoLayout.addWidget(self.copyInfoHashButton, 0, 2)
        sectionTwoLayout.addWidget(qtw.QLabel(), 0, 3)
        sectionTwoLayout.setColumnStretch(3, 1)

        sectionTwoWidget = qtw.QFrame()
        sectionTwoWidget.setLayout(sectionTwoLayout)


        closeAction = qtg.QAction(self)
        closeAction.setIcon(qtawesome.icon("msc.close"))
        closeAction.setData("close")
        closeAction.setToolTip("Close Panel")

        refreshAction = qtg.QAction(self)
        refreshAction.setIcon(qtawesome.icon("msc.refresh"))
        refreshAction.setData("refresh")
        refreshAction.setToolTip("Refresh")

        self.controlToolbar = qtw.QToolBar()
        self.controlToolbar.addAction(refreshAction)
        self.controlToolbar.addAction(closeAction)

        controlLayout = qtw.QHBoxLayout()
        controlLayout.addWidget(QWeightedColorLabel(color=appColors.dark_rgb, text="Torrent Info"))
        controlLayout.addStretch(1)
        controlLayout.addWidget(self.controlToolbar)

        controlWidget = qtw.QFrame()
        controlWidget.setObjectName("TorrentInfoWidgetControl")
        controlWidget.setLayout(controlLayout)

        bodyLayout = qtw.QVBoxLayout()
        bodyLayout.setContentsMargins(0, 0, 0, 0)
        bodyLayout.addWidget(controlWidget)
        bodyLayout.addWidget(sectionOneWidget)
        bodyLayout.addWidget(sectionTwoWidget)
        bodyLayout.addStretch()

        self.setLayout(bodyLayout)
        self.setObjectName('TorrentInfoWidget')
        self.setStyleSheet(loadStyle(":/qss/torrent_info.qss"))

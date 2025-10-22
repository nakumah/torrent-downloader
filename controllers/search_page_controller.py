import os

import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from py1337x.models import TorrentResult, TorrentItem, TorrentInfo

from core.signal_bus import signalBus
from core.structures import TorrentCategory, TorrentSortBy, BrowseTableColumns
from core.workers import getIconFromCategory
from views.pages.search_page import SearchPage


class SearchPageController(qtc.QObject):

    configReady = qtc.Signal()
    loadInfo = qtc.Signal()
    torrentClicked = qtc.Signal(str)
    downloadRequested = qtc.Signal(TorrentInfo)

    def __init__(self, view: SearchPage, parent=None):
        super().__init__(parent=parent)

        self.view = view

        self.__searchConfig: dict[str, ...] = {
            "page": 1,
            "sort_by": TorrentSortBy.SEEDERS,
            "category": TorrentCategory.TV,
            "torrent_id": None,
            "torrent_info": None,
        }

        self.__initialize()
        self.__configure()

    # region prime
    def __initialize(self):

        # populate category boxes
        self.view.categoryComboBox.addItem("Movies Only", TorrentCategory.MOVIES)
        self.view.categoryComboBox.addItem("TV Only", TorrentCategory.TV)
        self.view.categoryComboBox.addItem("Games Only", TorrentCategory.GAMES)
        self.view.categoryComboBox.addItem("Applications Only", TorrentCategory.APPS)
        self.view.categoryComboBox.addItem("Music Only", TorrentCategory.MUSIC)
        self.view.categoryComboBox.addItem("Documentaries Only", TorrentCategory.DOCUMENTARIES)
        self.view.categoryComboBox.addItem("Anime Only", TorrentCategory.ANIME)
        self.view.categoryComboBox.addItem("Other Only", TorrentCategory.OTHER)
        self.view.categoryComboBox.addItem("XXX Only", TorrentCategory.XXX)

        # populate sort by boxes
        self.view.sortByComboBox.addItem("Sort by Time", TorrentSortBy.TIME)
        self.view.sortByComboBox.addItem("Sort by Size", TorrentSortBy.SIZE)
        self.view.sortByComboBox.addItem("Sort by Seeders", TorrentSortBy.SEEDERS)
        self.view.sortByComboBox.addItem("Sort by Leechers", TorrentSortBy.LEECHERS)

        self.view.categoryComboBox.setCurrentIndex(1)
        self.view.sortByComboBox.setCurrentIndex(2)

        self.view.progressBar.hide()
        self.view.bottomWidget.show()

    # endregion

    # region configure
    def __configure(self):
        self.view.categoryComboBox.currentIndexChanged.connect(self.__handleCategoryComboBoxChanged)
        self.view.sortByComboBox.currentIndexChanged.connect(self.__handleSortComboBoxChanged)
        self.view.paginationToolbar.triggered.connect(self.__handlePaginationTriggered)

        self.view.torrentsTable.cellDoubleClicked.connect(self.__handleTableCellDoubleClicked)

        self.view.torrentInfoWidget.controlToolbar.actionTriggered.connect(self.__handleTorrentInfoToolbarTriggered)
        self.view.torrentInfoWidget.magnetDownloadButton.clicked.connect(self.__handleMagnetDownloadClicked)
        self.view.torrentInfoWidget.copyInfoHashButton.clicked.connect(self.__handleCopyInfoHashClicked)

    # endregion

    # region workers

    def showLoading(self, state):
        self.view.progressBar.setVisible(state)

    def populateTorrentInfo(self, data: TorrentInfo):

        self.__searchConfig["torrent_info"] = data

        print("[THUMBNAIL]", data.thumbnail)

        pixmap = qtg.QPixmap(":/images/torrent_file.png").scaled(128, 128)
        self.view.torrentInfoWidget.thumbnailLabel.setPixmap(pixmap)

        self.view.torrentInfoWidget.nameValueLabel.setText(data.name)
        self.view.torrentInfoWidget.categoryValueLabel.setText(data.category)
        self.view.torrentInfoWidget.typeValueLabel.setText(data.type)
        self.view.torrentInfoWidget.languageValueLabel.setText(data.language)
        self.view.torrentInfoWidget.totalSizeValueLabel.setText(data.size)
        self.view.torrentInfoWidget.uploadedByValueLabel.setText(data.uploader)
        self.view.torrentInfoWidget.downloadsValueLabel.setText(data.downloads)
        self.view.torrentInfoWidget.lastCheckedValueLabel.setText(data.last_checked)
        self.view.torrentInfoWidget.dateUploadedValueLabel.setText(data.date_uploaded)
        self.view.torrentInfoWidget.seedersValueLabel.setText(data.seeders)
        self.view.torrentInfoWidget.leechersValueLabel.setText(data.leechers)
        self.view.torrentInfoWidget.infoHashValueLabel.setText(data.info_hash)

    def populateTorrentTable(self, data: TorrentResult, category: TorrentCategory):
        # update the page counts
        self.view.paginationToolbar.setTotalPages(data.page_count)
        self.view.paginationToolbar.setCurrentPage(data.current_page)

        # populate the table
        self.view.torrentsTable.resetTable()
        self.view.torrentsTable.setRowCount(data.item_count)

        for row in range(data.item_count):
            torrentItem: TorrentItem = data.items[row]
            icon = getIconFromCategory(category)

            name_entry = torrentItem.name
            collapsed_entry = qtg.QFontMetrics(self.view.torrentsTable.font()).elidedText(
                name_entry,
                qtc.Qt.TextElideMode.ElideRight,
                int(self.view.torrentsTable.columnWidth(BrowseTableColumns.NAME) * 2.5),
            )
            nameItem = qtw.QTableWidgetItem(icon, collapsed_entry)
            nameItem.setToolTip(name_entry)
            nameItem.setData(qtg.Qt.ItemDataRole.UserRole, torrentItem.torrent_id)

            seedersItem = qtw.QTableWidgetItem(torrentItem.seeders)
            leechersItem = qtw.QTableWidgetItem(torrentItem.leechers)
            timeItem = qtw.QTableWidgetItem(torrentItem.time)
            sizeItem = qtw.QTableWidgetItem(torrentItem.size)
            uploaderItem = qtw.QTableWidgetItem(torrentItem.uploader)

            self.view.torrentsTable.setItem(row, BrowseTableColumns.NAME, nameItem)
            self.view.torrentsTable.setItem(row, BrowseTableColumns.SEEDERS, seedersItem)
            self.view.torrentsTable.setItem(row, BrowseTableColumns.LEECHERS, leechersItem)
            self.view.torrentsTable.setItem(row, BrowseTableColumns.TIME, timeItem)
            self.view.torrentsTable.setItem(row, BrowseTableColumns.SIZE, sizeItem)
            self.view.torrentsTable.setItem(row, BrowseTableColumns.UPLOADER, uploaderItem)

    def __flagTorrent(self, row: int):
        nameItem: qtw.QTableWidgetItem = self.view.torrentsTable.item(row, 0)
        torrent_id: str = nameItem.data(qtg.Qt.ItemDataRole.UserRole)
        self.__searchConfig["torrent_id"] = torrent_id
    # endregion

    # region event handlers

    # region torrent info
    def __handleTorrentInfoToolbarTriggered(self, action: qtg.QAction):
        if action.data() == "close":
            self.view.bottomWidget.hide()

        if action.data() == "refresh":
            self.loadInfo.emit()

    def __handleMagnetDownloadClicked(self):
        torrentInfo = self.__searchConfig.get("torrent_info", None)
        if not isinstance(torrentInfo, TorrentInfo):
            qtw.QMessageBox.information(
                self.view,
                "Torrent Info",
                "Not a valid torrent, use search to trigger valid torrent"
            )
            return

        saveLocation = os.path.join(os.getcwd(), "AppData")
        exitCode = self.view.previewDialog.launch(torrentInfo, saveLocation)
        if exitCode != qtw.QDialog.DialogCode.Accepted:
            return

        saveFolder: str = self.view.previewDialog.saveFolder()
        if saveFolder is None:
            qtw.QMessageBox.critical(self.view, "Save Directory", "Provided save folder does not exist")
            return

        self.downloadRequested.emit(torrentInfo)

    def __handleCopyInfoHashClicked(self):
        text = self.view.torrentInfoWidget.infoHashValueLabel.text()
        signalBus.CopyToClipboard.emit(text)

    # endregion

    # region search

    def __handleCategoryComboBoxChanged(self, index: int) -> None:
        self.__searchConfig["category"] = self.view.categoryComboBox.itemData(index)
        self.configReady.emit()

    def __handleSortComboBoxChanged(self, index: int) -> None:
        self.__searchConfig["sort_by"] = self.view.sortByComboBox.itemData(index)
        self.configReady.emit()

    def __handlePaginationTriggered(self, page: int) -> None:
        self.__searchConfig["page"] = page
        self.configReady.emit()

    def __handleTableCellClicked(self, row: int, _: int) -> None:
        self.__flagTorrent(row)

    def __handleTableCellDoubleClicked(self, row: int, _: int) -> None:
        self.__flagTorrent(row)
        self.loadInfo.emit()

    # endregion

    # endregion

    # region setters

    def setTotalPages(self, value: int) -> None:
        self.view.paginationToolbar.setTotalPages(value)

    def setCurrentPage(self, value: int) -> None:
        self.view.paginationToolbar.setCurrentPage(value)

    # endregion

    # region getters
    def searchConfig(self):
        return self.__searchConfig
    # endregion


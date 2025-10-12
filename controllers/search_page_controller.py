import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from py1337x.models import TorrentResult, TorrentItem

from core.structures import TorrentCategory, TorrentSortBy, BrowseTableColumns
from core.workers import getIconFromCategory
from views.pages.search_page import SearchPage


class SearchPageController(qtc.QObject):

    configReady = qtc.Signal()

    def __init__(self, view: SearchPage, parent=None):
        super().__init__(parent=parent)

        self.view = view

        self.__searchConfig: dict[str, str | int] = {
            "page": 1,
            "sort_by": TorrentSortBy.SEEDERS,
            "category": TorrentCategory.TV,
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

    # endregion

    # region configure
    def __configure(self):
        self.view.categoryComboBox.currentIndexChanged.connect(self.__handleCategoryComboBoxChanged)
        self.view.sortByComboBox.currentIndexChanged.connect(self.__handleSortComboBoxChanged)
        self.view.paginationToolbar.triggered.connect(self.__handlePaginationTriggered)

    # endregion

    # region workers
    def showLoading(self, state):
        self.view.progressBar.setVisible(state)

    def populate(self, data: TorrentResult, category: TorrentCategory):
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

    def __trigger(self):
        self.configReady.emit()

    # endregion

    # region event handlers

    def __handleCategoryComboBoxChanged(self, index: int) -> None:
        self.__searchConfig["category"] = self.view.categoryComboBox.itemData(index)
        self.__trigger()

    def __handleSortComboBoxChanged(self, index: int) -> None:
        self.__searchConfig["sort_by"] = self.view.sortByComboBox.itemData(index)
        self.__trigger()

    def __handlePaginationTriggered(self, page: int) -> None:
        self.__searchConfig["page"] = page
        self.__trigger()

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


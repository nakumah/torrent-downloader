from PySide6.QtWidgets import QApplication
from py1337x.models import TorrentResult, TorrentInfo

from controllers.search_page_controller import SearchPageController
from core.signal_bus import signalBus
from core.structures import NavPages, TorrentCategory, TorrentSortBy
from core.utils.thread_manager import TheadManager
from core.utils.torrent_manager import TorrentManager
from models.worker_thread import WorkerThread
from models.worker_thread_data_model import WorkerThreadDataModel
from views.main_window import MainWindow


class MainController:
    def __init__(self, view: MainWindow, app: QApplication):

        self.TORRENT_MANAGER = TorrentManager()
        self.THREAD_MANAGER = TheadManager()

        self.app = app
        self.view = view

        self.searchPageController = SearchPageController(view=view.navStack.getPage(NavPages.SEARCH))

        self.__searchConfig: dict[str, ...] = {
            "page": 1,
            "sort_by": TorrentSortBy.SEEDERS,
            "category": TorrentCategory.TV,
            "query": "",
            "weekly": False,
            "link": None,
            "torrent_id": None,
        }

        self.__initialize()
        self.__configure()
        self.__connectSignals()

    # region initialize

    def __initialize(self):
        self.TORRENT_MANAGER.initialize()
        self.view.navStack.setCurrentPage(NavPages.SEARCH)

    # endregion

    # region configure

    def __configure(self):
        self.view.navPanel.panelBtnTriggered.connect(self.__handlePanelTriggered)
        self.view.customTitleBar.searchInput.searchReady.connect(self.__handleSearchInputReady)
        self.searchPageController.configReady.connect(self.__handleSearchConfigReady)
        self.searchPageController.loadInfo.connect(self.__handleLoadTorrentInfo)
        self.searchPageController.downloadRequested.connect(self.__handleDownloadClicked)

    # endregion

    # region workers

    def __updateSearchConfig(self, conf: dict[str, str | int]):

        for k in conf.keys():
            if k not in self.__searchConfig.keys():
                raise KeyError("Invalid key <{}>, accepted: {}".format(k, self.__searchConfig.keys()))

        self.__searchConfig.update(conf)

    # region query search endpoint

    def onQuerySearchStart(self, _=None):
        self.searchPageController.showLoading(True)

    def onQuerySearchSuccessful(self, res: TorrentResult):
        self.searchPageController.populateTorrentTable(res, self.__searchConfig['category'])
        self.searchPageController.showLoading(False)

    def onQuerySearchError(self, error):
        self.searchPageController.showLoading(False)
        print("QUERY ERROR: {}".format(error))

    def querySearchEndpoint(self):

        model = WorkerThreadDataModel(
            pid="query-search", on_success=self.onQuerySearchSuccessful, on_error=self.onQuerySearchError,
            on_start=self.onQuerySearchStart, task_params=self.__searchConfig, task=self.TORRENT_MANAGER.search, override=True
        )
        thread = WorkerThread(model=model)
        signalBus.launchThread.emit(thread)

    # endregion

    # region query info endpoint

    def onQueryInfoStart(self, _=None):
        self.searchPageController.showLoading(True)

    def onQueryInfoSuccessful(self, res: TorrentInfo):
        self.searchPageController.view.bottomWidget.show()
        self.searchPageController.populateTorrentInfo(res)
        self.searchPageController.showLoading(False)

    def onQueryInfoError(self, error):
        self.searchPageController.showLoading(False)
        print("QUERY ERROR: {}".format(error))

    def queryInfoEndpoint(self):
        if self.__searchConfig.get("torrent_id") is None:
            return

        model = WorkerThreadDataModel(
            pid="query-info", on_success=self.onQueryInfoSuccessful, on_error=self.onQueryInfoError,
            on_start=self.onQueryInfoStart, task_params=self.__searchConfig, task=self.TORRENT_MANAGER.info, override=True
        )
        thread = WorkerThread(model=model)
        signalBus.launchThread.emit(thread)

    # endregion

    # endregion

    # region event handlers
    def __handleDownloadClicked(self, info: TorrentInfo):
        pass

    def __handleLoadTorrentInfo(self):
        self.__searchConfig["torrent_id"] = self.searchPageController.searchConfig().get("torrent_id", None)
        self.queryInfoEndpoint()

    def __handleSearchConfigReady(self):
        self.__updateSearchConfig(self.searchPageController.searchConfig())
        self.querySearchEndpoint()

    def __handleSearchInputReady(self, text: str):
        self.view.navStack.setCurrentPage(NavPages.SEARCH)
        self.__updateSearchConfig({'query': text})
        self.querySearchEndpoint()

    def __handlePanelTriggered(self, page: NavPages):
        self.view.navStack.setCurrentPage(page)

    def __handleCopyToClipboard(self, value: object):
        clipboard = self.app.clipboard()
        clipboard.setText(str(value))

    # endregion


    # region connect signals

    def __connectSignals(self):
        signalBus.CopyToClipboard.connect(self.__handleCopyToClipboard)

    # endregion
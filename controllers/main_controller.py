from py1337x.models import TorrentResult

from controllers.search_page_controller import SearchPageController
from core.signal_bus import signalBus
from core.structures import NavPages, TorrentCategory, TorrentSortBy
from core.utils.thread_manager import TheadManager
from core.utils.torrent_manager import TorrentManager
from models.worker_thread import WorkerThread
from models.worker_thread_data_model import WorkerThreadDataModel
from views.main_window import MainWindow


class MainController:
    def __init__(self, view: MainWindow):

        self.TORRENT_MANAGER = TorrentManager()
        self.THREAD_MANAGER = TheadManager()

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

    # endregion

    # region workers

    def __updateSearchConfig(self, conf: dict[str, str | int]):

        for k in conf.keys():
            if k not in self.__searchConfig.keys():
                raise KeyError("Invalid key <{}>, accepted: {}".format(k, self.__searchConfig.keys()))

        self.__searchConfig.update(conf)

    # region query endpoint

    def onQueryStart(self, _=None):
        self.searchPageController.showLoading(True)

    def onQuerySuccessful(self, res: TorrentResult):
        self.searchPageController.populate(res, self.__searchConfig['category'])
        self.searchPageController.showLoading(False)

    def onQueryError(self, error):
        self.searchPageController.showLoading(False)
        print("QUERY ERROR: {}".format(error))

    def queryEndpoint(self):

        model = WorkerThreadDataModel(
            pid="search", on_success=self.onQuerySuccessful, on_error=self.onQueryError,
            on_start=self.onQueryStart, task_params=self.__searchConfig, task=self.TORRENT_MANAGER.search, override=True
        )
        thread = WorkerThread(model=model)
        signalBus.launchThread.emit(thread)


    # endregion

    # endregion

    # region event handlers
    def __handleSearchConfigReady(self):
        self.__updateSearchConfig(self.searchPageController.searchConfig())
        self.queryEndpoint()

    def __handleSearchInputReady(self, text: str):
        self.view.navStack.setCurrentPage(NavPages.SEARCH)
        self.__updateSearchConfig({'query': text})
        self.queryEndpoint()

    def __handlePanelTriggered(self, page: NavPages):
        self.view.navStack.setCurrentPage(page)

    # endregion
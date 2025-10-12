from core.signal_bus import signalBus
from core.structures import NavPages, TorrentCategory
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

    # endregion

    # region workers

    # region query endpoint

    def onQueryStart(self, _=None):
        print("querying endpoint")
        # silo s01 complete

    def onQuerySuccessful(self, res):
        print("[QUERY SUCCESSFUL]: {}".format(res))

    def onQueryError(self, error):
        print("QUERY ERROR: {}".format(error))

    def queryTask(self, conf: dict[str, str | int]):
        _conf = {
            'query': "",
            'page': 1,
            'order': 'desc'
        }
        _conf.update(conf)
        return self.TORRENT_MANAGER.search(_conf)

    def queryEndpoint(self, value: str):
        params = {'query': value}
        model = WorkerThreadDataModel(
            pid="search", on_success=self.onQuerySuccessful, on_error=self.onQueryError,
            on_start=self.onQueryStart, task_params=params, task=self.queryTask, override=True
        )
        thread = WorkerThread(model=model)
        signalBus.launchThread.emit(thread)


    # endregion

    # endregion

    # region event handlers
    def __handleSearchInputReady(self, text: str):
        self.queryEndpoint(text)

    def __handlePanelTriggered(self, page: NavPages):
        self.view.navStack.setCurrentPage(page)

    # endregion
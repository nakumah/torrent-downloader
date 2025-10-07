from core.structures import NavPages
from views.main_window import MainWindow


class MainController:
    def __init__(self, view: MainWindow):

        self.view = view


        self.__initialize()
        self.__configure()

    # region initialize

    def __initialize(self):
        self.view.navStack.setCurrentPage(NavPages.SEARCH)

    # endregion

    # region configure

    def __configure(self):
        self.view.navPanel.panelBtnTriggered.connect(self.__handlePanelTriggered)

    # endregion

    # region event handlers

    def __handlePanelTriggered(self, page: NavPages):
        self.view.navStack.setCurrentPage(page)

    # endregion
import PySide6.QtWidgets as qtw

from resources.styling import loadStyle


class SettingsPage(qtw.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        pageTitle = qtw.QLabel("Settings")
        pageTitle.setObjectName('PageTitle')

        pageLayout = qtw.QGridLayout()
        pageLayout.setContentsMargins(20, 30, 20, 10)

        pageLayout.addWidget(pageTitle)

        self.setLayout(pageLayout)

        self.setObjectName("SettingsPage")
        self.setStyleSheet(loadStyle(":/qss/settings_page.qss"))
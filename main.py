import os
import sys

from PySide6.QtWidgets import QApplication

from controllers.main_controller import MainController
from resources import resources_rc #type: ignore

from views.main_window import MainWindow

os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"  # disable dark mode support


def main():
    app = QApplication(sys.argv)
    controller = MainController(MainWindow(), app)
    controller.view.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

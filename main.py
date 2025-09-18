import os
import sys

from PySide6.QtWidgets import QApplication

from resources import resources_rc #type: ignore

from views.main_window import MainWindow

os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"  # disable dark mode support


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

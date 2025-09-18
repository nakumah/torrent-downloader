from PySide6.QtCore import QFile, QTextStream
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPalette


from resources.app_colors import AppColors


def parseStyle(qss: str) -> str:
    """
    Parses the style,
    replaces all keywords with their corresponding values

    Arguments:
        qss (str): the style string

    Returns:
        str: the parsed style string

    """

    for name in dir(AppColors):
        if not name.startswith("_"):
            value = getattr(AppColors, name)
            if isinstance(value, str):
                qss = qss.replace(name, value)
    return qss


def loadStyle(path : str) -> str:
    """
    Loads style from a qss file

    Arguments:
        path (str): the qss path to the qss file

    Returns:
        str: the parsed style string

    Raises:
        IOError: if the qss file does not exist
        TypeError: if an invalid type is provided
    """
    if isinstance(path, str):
        file = QFile(path)
    else:
        raise TypeError("expected str, got {}".format(type(path)))

    if not file.open(QFile.OpenModeFlag.ReadOnly):
        raise IOError(f"Could not open QSS file: {path}")

    stream = QTextStream(file)
    qss = stream.readAll()
    file.close()

    return parseStyle(qss)


def changeWidgetBackground(widget: QWidget, color: str):
    """
    Sets the background of the widget to color
    :param widget:
    :param color:
    :return:
    """
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    widget.setPalette(palette)

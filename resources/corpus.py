from io import StringIO
from PySide6.QtCore import QFile, QTextStream

import pandas as pd

def loadCorpus(path: str) -> str:

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

    return qss


def loadExtensionsCSV() -> pd.DataFrame:
    """
    loads the file extensions from the corpus
    :return:
    """
    csv_string = loadCorpus(":/corpus/extensions.csv")
    df = pd.read_csv(StringIO(csv_string), delimiter=",", dtype=str)
    return df


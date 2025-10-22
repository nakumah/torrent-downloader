import os
import sqlite3
import traceback

import PySide6.QtCore as qtc

from core.signal_bus import signalBus
from core.utils.database.database_thread import DatabaseThread, DatabaseThreadActions
from models.database_worker_data_model import DatabaseWorkerDataModel


class DatabaseManager(qtc.QObject):
    def __init__(self, db_file: str = None, parent: qtc.QObject = None, ):
        super().__init__(parent=parent)

        self.__file = db_file
        self.__dbThread = DatabaseThread()
        self.__models: dict[str, DatabaseWorkerDataModel] = {}

        self.__configure()

    def initialize(self):

        if not isinstance(self.__file, str):
            raise ValueError("Db file is not a string, got {}".format(type(self.__file)))

        if not os.path.exists(os.path.dirname(self.__file)):
            raise FileNotFoundError(f"Parent folder <{os.path.dirname(self.__file)}> doesn't exist")

        if not os.path.exists(self.__file):
            conn = sqlite3.connect(self.__file)
            conn.close()

        # spawn a new connection to the database and prime it
        # for multiple thread access.
        conn = sqlite3.connect(self.__file, check_same_thread=False)
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.commit()
        finally:
            conn.close()

        self.__dbThread.setFile(self.__file)
        self.__dbThread.start()

    def __configure(self):
        self.__dbThread.started.connect(self.__handleThreadStarted)
        self.__dbThread.finished.connect(self.__handleThreadFinished)

        self.__dbThread.executionError.connect(self.__handleExecutionError)
        self.__dbThread.queryStarted.connect(self.__handleQueryStarted)
        self.__dbThread.querySuccess.connect(self.__handleQuerySuccess)
        self.__dbThread.queryError.connect(self.__handleQueryError)
        self.__dbThread.queryFinished.connect(self.__handleQueryFinished)

    # region workers

    def launchQuery(self, model: DatabaseWorkerDataModel, action: DatabaseThreadActions):

        # queue the data into the thread
        self.__models[model.wid] = model
        self.__dbThread.addTask(model, action)

    # endregion

    # region event handlers
    def __handleThreadStarted(self):
        signalBus.LogToConsole.emit(("Database thread started", "warning"))

    def __handleThreadFinished(self):
        signalBus.LogToConsole.emit(("Database thread finished", "info"))

    def __handleExecutionError(self, e: Exception):
        error_string = "[EXECUTION_ERROR_DB_MANAGER] " + str(e) + "\n"
        for line in traceback.format_tb(e.__traceback__):
            error_string += line

        # signalBus.CreateLogEntry.emit(error_string)
        signalBus.LogToConsole.emit((error_string, "error"))

    def __handleQuerySuccess(self, args: tuple[str, object]):
        modelId, _ = args
        model = self.__models.get(modelId, None)
        if model is None:
            return
        model.on_success(args)

    def __handleQueryError(self, args: tuple[str, Exception]):

        modelId, _ = args
        model = self.__models.get(modelId, None)
        if model is None:
            return
        model.on_error(args)

    def __handleQueryStarted(self, modelId: str):
        model = self.__models.get(modelId, None)
        if model is None:
            return
        model.on_start(modelId)

    def __handleQueryFinished(self, modelId: str):

        model = self.__models.pop(modelId, None)
        if model is None:
            return

        model.on_finish(modelId)
        model.deleteLater()

    def __handleQueryDatabase(self, opts: dict[str, object]):
        self.launchQuery(**opts)

    # endregion

    # region getters

    def file(self):
        return self.__file

    # endregion

    # region setters

    def setFile(self, db_file: str):
        parentFolder = os.path.dirname(db_file)
        assert (os.path.isdir(parentFolder)), f"Parent folder {parentFolder} doesn't exist"

        self.__file = db_file

    def setDbThread(self, dbThread: DatabaseThread):
        self.__dbThread = dbThread

    # endregion

    # region connect signals

    def __connectSignals(self):
        signalBus.QueryDatabase.connect(self.__handleQueryDatabase)

    # endregion

import sqlite3
import uuid

from PySide6.QtCore import QObject, QRunnable, Signal

from models.database_worker_data_model import DatabaseWorkerDataModel


class DatabaseThreadPoolRunnerSignals(QObject):
    # Each signals the thread id and the corresponding value
    started = Signal(str)  # str -> thread id
    failed = Signal(tuple)  # tuple[str, Exception] -> thread id, error
    completed = Signal(tuple)  # str -> thread id, result of task executed
    finished = Signal(str)  # str -> thread id


class DatabaseThreadPoolRunner(QRunnable):

    def __init__(self, model: DatabaseWorkerDataModel, conn: sqlite3.Connection):
        super().__init__()

        self.__model = model
        self.__conn = conn
        self.__runnerId = str(uuid.uuid4())
        self.signals = DatabaseThreadPoolRunnerSignals()

    # region override

    def run(self):
        try:
            self.signals.started.emit(self.__model.wid)
            result = self.__model.fn(self.__conn, **self.__model.args)
            self.__conn.commit()
            self.signals.completed.emit((self.__model.wid, result))
        except Exception as e:
            self.__conn.rollback()
            self.signals.failed.emit((self.__model.wid, e))
        finally:
            self.__conn.close()
            self.signals.finished.emit(self.__model.wid)

    # endregion

    # region getters
    def runnerId(self) -> str:
        return self.__runnerId

    def pid(self) -> str:
        return self.__model.workerId()

    def threadId(self) -> str:
        return self.__model.workerId()

    def model(self) -> DatabaseWorkerDataModel:
        return self.__model

    # endregion

    # region setters

    def setModel(self, model: DatabaseWorkerDataModel):
        self.__model = model

    # endregion

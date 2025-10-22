import enum
import sqlite3
from queue import Queue

import PySide6.QtCore as qtc

from core.utils.database.database_thread_pool_runner import DatabaseThreadPoolRunner
from models.database_worker_data_model import DatabaseWorkerDataModel


class DatabaseThreadActions(enum.StrEnum):
    TERMINATE = "TERMINATE"
    STOP = "STOP"
    QUIT = "QUIT"
    READ = "READ"
    WRITE = "WRITE"


class DatabaseThread(qtc.QThread):
    executionError = qtc.Signal(Exception)

    queryStarted = qtc.Signal(str)
    querySuccess = qtc.Signal(tuple)
    queryError = qtc.Signal(tuple)
    queryFinished = qtc.Signal(str)

    def __init__(self):
        super().__init__()
        self.__file: str | None = None
        self.__running: bool = True

        self.__readThreadPool: qtc.QThreadPool = qtc.QThreadPool.globalInstance()

        self.__readTaskQueue: Queue[DatabaseWorkerDataModel] = Queue()
        self.__writeTaskQueue: Queue[DatabaseWorkerDataModel] = Queue()
        self.__operationQueue: Queue[DatabaseThreadActions] = Queue()

    # region Core

    def __run__(self):
        while self.__running:

            # block and wait for new thread actions if queue is empty.
            action: DatabaseThreadActions = self.__operationQueue.get()

            if action == DatabaseThreadActions.READ:

                # if the read queue is empty, skip
                if self.__readTaskQueue.empty():
                    continue

                # unpack all read data tasks in the queue
                # this will run them simultaneously

                # create a pool for this read batch
                while not self.__readTaskQueue.empty():
                    # acquire the data
                    data = self.__readTaskQueue.get()
                    conn = self.__makeConnection()

                    # instantiate and configure the runner
                    runner = DatabaseThreadPoolRunner(data, conn)
                    runner.signals.started.connect(self.__handleRunnerStarted)
                    runner.signals.completed.connect(self.__handleRunnerSuccess)
                    runner.signals.failed.connect(self.__handleRunnerError)
                    runner.signals.finished.connect(self.__handleRunnerFinished)

                    # invoke the runner in the thread pool
                    self.__readThreadPool.start(runner)

            elif action == DatabaseThreadActions.WRITE:
                # get the current task definition and execute on this thread.
                if self.__writeTaskQueue.empty():
                    continue

                # get the corresponding data entry
                data = self.__writeTaskQueue.get()
                conn = self.__makeConnection()
                try:
                    self.queryStarted.emit(data.wid)
                    result = data.fn(conn, **data.args)
                    conn.commit()
                    self.querySuccess.emit((data.wid, result))
                except Exception as e:
                    conn.rollback()
                    self.queryError.emit((data.wid, e))
                finally:
                    conn.close()
            elif action == DatabaseThreadActions.STOP:
                # break out of the loop and terminate the execution.
                break
            else:
                raise ValueError("[Unhandled Actions] {}".format(action))

    def run(self) -> None:
        try:
            self.__run__()
        except Exception as e:
            self.executionError.emit(e)

    # endregion

    # region helpers
    def __makeConnection(self) -> sqlite3.Connection:
        # at this point, we assume that the file exists and is valid!!!!!
        return sqlite3.connect(self.__file, check_same_thread=False)

    # endregion

    # region workers
    def addTask(self, model: DatabaseWorkerDataModel, action: DatabaseThreadActions):
        if action == DatabaseThreadActions.READ:
            self.__readTaskQueue.put(model)
            self.__operationQueue.put(action)

        if action == DatabaseThreadActions.WRITE:
            self.__writeTaskQueue.put(model)
            self.__operationQueue.put(action)


    def stop(self):
        self.__running = False
        self.__operationQueue.put(DatabaseThreadActions.STOP)

    # endregion

    # region event handlers

    def __handleRunnerFinished(self, _id: str):

        # flag the runner as finished
        self.queryFinished.emit(_id)
        # try:
        #     # disconnect signals
        #     runner.signals.started.disconnect(self.queryStarted.emit)
        #     runner.signals.completed.disconnect(self.querySuccess.emit)
        #     runner.signals.failed.disconnect(self.queryError.emit)
        #     runner.signals.finished.disconnect(self.__handleRunnerFinished)
        # except Exception as e:
        #     self.executionError.emit(e)

    def __handleRunnerStarted(self, _id: str):
        self.queryStarted.emit(_id)

    def __handleRunnerSuccess(self, _opts: tuple):
        self.querySuccess.emit(_opts)

    def __handleRunnerError(self, _opts: tuple):
        self.queryError.emit(_opts)

    # endregion

    # region setters
    def setFile(self, file: str):
        self.__file = file

    # endregion

    # region getters

    def file(self):
        return self.__file

    def isWorking(self):
        return self.__running

    # endregion

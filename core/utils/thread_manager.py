from core.signal_bus import signalBus
from models.worker_thread import WorkerThread


class TheadManager:
    def __init__(self):

        self.__workerThreads: dict[str, WorkerThread] = {}
        self.__connectSignals()

    # region workers

    def __threadExists(self, tid: str) -> bool:
        return tid in self.__workerThreads.keys()

    def __canOverride(self, wt: WorkerThread) -> bool:
        """ checks if we can override the given thread """

        # if no thread with same id, return true
        if not self.__threadExists(wt.workerId()):
            return True

        # if the thread exists, check if the override flag is raised
        if wt.override():
            return True

        return False

    def __purge(self, tid: str) -> None:
        if not self.__threadExists(tid):
            return

        # acquire thread and mark for deleting
        t = self.__workerThreads.pop(tid)

        t.workerStarted.disconnect(self.__handleWorkerStarted)
        t.workerFinished.disconnect(self.__handleWorkerFinished)

        if t.isRunning():
            t.terminate()
        t.deleteLater()

    def launchThread(self, thread: WorkerThread):

        # check for thread override on existing running threads
        if not self.__canOverride(thread):
            return

        # if we can override, remove the old from the manager
        self.__purge(thread.workerId())

        # connect signals
        thread.workerStarted.connect(self.__handleWorkerStarted)
        thread.workerFinished.connect(self.__handleWorkerFinished)

        # collect thread
        self.addWorker(thread)

        # start the thread
        thread.start()

    def terminateThread(self, tid: str):
        if not self.__threadExists(tid):
            return
        self.__purge(tid)

    def stopThread(self, tid: str):
        if not self.__threadExists(tid):
            return

        t = self.__workerThreads.pop(tid)
        t.quit()

        self.__purge(tid)

    # endregion

    # region event handlers

    def __handleWorkerStarted(self, tid: str) -> None:
        if not self.__threadExists(tid):
            return

        wt = self.__workerThreads[tid]
        on_start = wt.model().onStart()
        on_start(None)

    def __handleWorkerFinished(self, tid: str) -> None:
        if not self.__threadExists(tid):
            return

        wt = self.__workerThreads[tid]
        err = wt.model().taskError()
        if isinstance(err, Exception):
            on_error = wt.model().onError()
            on_error(err)
        else:
            on_success = wt.model().onSuccess()
            task_res = wt.model().taskResults()
            on_success(task_res)

        self.__purge(tid)

    def __handleTerminateThread(self, tid: str) -> None:
        self.terminateThread(tid)

    def __handleStopThread(self, tid: str) -> None:
        self.stopThread(tid)

    def __handleLaunchThread(self, thread: WorkerThread):
        assert isinstance(thread, WorkerThread), f"Expected WorkerThread, got {type(thread)}"
        self.launchThread(thread)

    # endregion

    # region getters
    def worker(self, worker_id: str) -> WorkerThread | None:
        return self.__workerThreads.get(worker_id, None)

    # endregion

    # region setters

    def addWorker(self, worker: WorkerThread) -> None:
        self.__workerThreads[worker.workerId()] = worker

    # endregion

    # region connect Signals
    def __connectSignals(self):
        signalBus.launchThread.connect(self.__handleLaunchThread)
        signalBus.terminateThread.connect(self.__handleTerminateThread)
        signalBus.stopThread.connect(self.__handleStopThread)
    # endregion



import PySide6.QtCore as qtc

from models.worker_thread_data_model import WorkerThreadDataModel


class WorkerThread(qtc.QThread):

    workerStarted = qtc.Signal(str)
    workerFinished = qtc.Signal(str)

    def __init__(self, parent=None, model: WorkerThreadDataModel = None):
        super().__init__(parent=parent)

        self.__model: WorkerThreadDataModel = model or WorkerThreadDataModel()

        self.started.connect(lambda: self.workerStarted.emit(self.__model.modelId()))
        self.finished.connect(lambda: self.workerFinished.emit(self.__model.modelId()))

    def run(self):
        try:
            task = self.__model.task()
            params = self.__model.taskParams()
            res = task(params)
            self.__model.setOpts(task_results=res)
        except Exception as e:
            self.__model.setOpts(task_error=e)

    def model(self) -> WorkerThreadDataModel:
        return self.__model

    def setModel(self, model: WorkerThreadDataModel):
        self.__model = model

    def workerId(self):
        """ Worker ID is the corresponding model id """
        return self.__model.modelId()

    def override(self) -> bool:
        return self.__model.opt("override")
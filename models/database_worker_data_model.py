import sqlite3
import typing
import uuid

import PySide6.QtCore as qtc

P = typing.ParamSpec("P")
R = typing.TypeVar("R")

TaskType = typing.Callable[[typing.Concatenate[sqlite3.Connection, P]], typing.Any]
TaskArgsType = dict[str, typing.Any]
HandlerType = typing.Callable[[typing.Optional[typing.Union[Exception, typing.Any]]], typing.Any]


class Handlers(typing.TypedDict, total=False):
    on_start: HandlerType
    on_success: HandlerType
    on_error: HandlerType
    on_finish: HandlerType


class DatabaseWorkerDataModel(qtc.QObject):
    def __init__(self,
                 task: TaskType,
                 taskArgs: TaskArgsType,
                 handlers: Handlers,
                 workerId: str = None
                 ) -> None:
        super().__init__()
        self.__workerId = workerId or str(uuid.uuid4())
        self.__task: TaskType = lambda _=None: None
        self.__taskArgs: TaskArgsType = {}
        self.__handlers: Handlers = {
            "on_start": self.__void__,
            "on_success": self.__void__,
            "on_error": self.__void__,
            "on_finish": self.__void__,
        }

        self.setProperties(task, taskArgs, handlers)

    # region properties

    @staticmethod
    def __void__(_=None):
        return

    @property
    def wid(self):
        return self.__workerId

    @property
    def fn(self):
        return self.__task

    @property
    def args(self):
        return self.__taskArgs

    @property
    def on_start(self) -> HandlerType:
        return self.__handlers["on_start"]

    @property
    def on_success(self) -> HandlerType:
        return self.__handlers["on_success"]

    @property
    def on_error(self) -> HandlerType:
        return self.__handlers["on_error"]

    @property
    def on_finish(self) -> HandlerType:
        return self.__handlers["on_finish"]

    # endregion

    # region getters

    def workerId(self) -> str:
        return self.__workerId

    def task(self) -> TaskType:
        return self.__task

    def taskArgs(self) -> TaskArgsType:
        return self.__taskArgs

    def handlers(self) -> Handlers:
        return self.__handlers

    def handler(self, name: str) -> HandlerType:

        if name == "on_start":
            return self.on_start
        elif name == "on_success":
            return self.on_success
        elif name == "on_error":
            return self.on_error
        elif name == "on_finish":
            return self.on_finish
        else:
            raise KeyError(f"Invalid handler name: {name}. Accepted handlers: {self.__handlers.keys()}")

    # endregion

    # region setters

    def setWorkerId(self, workerId: str):
        self.__workerId = workerId

    def setHandlers(self, handlers: Handlers) -> None:
        self.__validateHandlers(handlers)
        self.__handlers.update(handlers)

    def setTask(self, task: TaskType) -> None:
        self.__validateTask(task)
        self.__task = task

    def setTaskArgs(self, taskArgs: TaskArgsType) -> None:
        self.__validateTaskArgs(taskArgs)
        self.__taskArgs = taskArgs

    def setProperties(self,
                      task: TaskType,
                      taskArgs: TaskArgsType,
                      handlers: Handlers
                      ):
        self.setTask(task)
        self.setTaskArgs(taskArgs)
        self.setHandlers(handlers)

    # endregion

    # region validate
    def __validateHandlers(self, handlers):
        assert isinstance(handlers, dict), "handlers must be a dictionary"
        assert (0 <= len(handlers) <= 4), "handlers must have at most 4 arguments"

        if len(handlers) > 0:
            for key, fn in handlers.items():
                assert isinstance(key, str), "key must be a string"
                assert key in list(
                    self.__handlers.keys()), f"Invalid handler name: <{key}>, accepted names are {list(self.__handlers.keys())}"

                assert isinstance(fn, typing.Callable), f"Expected callable, got <{type(fn)}>"

    def __validateTask(self, fn):
        assert isinstance(fn, typing.Callable), "task must be a function that takes any number of arguments"

    def __validateTaskArgs(self, taskArgs):
        assert isinstance(taskArgs,
                          dict), "taskArgs must be a dictionary whose keys must match argument names in the task signature"

    # endregion

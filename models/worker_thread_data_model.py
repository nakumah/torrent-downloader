import typing
import uuid


class WorkerThreadDataModel:
    accepted_keys = ["pid", "on_success", "on_start", "on_error", "task_params", "task",
                     "task_results", "task_error", "override"]

    def __init__(self, **kwargs):

        self._opts = {}

        self.setOpts(**kwargs)

        # assign a default id
        if self._opts.get("pid", None) is None:
            self._opts["pid"] = str(uuid.uuid4())

    # region setters
    def setOpts(self, **kwargs):
        for arg, val in kwargs.items():

            self.__validateKey(arg)

            if arg in ["on_success", "on_start", "on_error", "task"]:
                assert isinstance(val, typing.Callable)

            if arg == "override":
                assert isinstance(val, bool), "Override must be a boolean"

            self._opts[arg] = val

    # endregion

    # region getters

    def getOpts(self):
        return self._opts

    def opt(self, key: str):
        self.__validateKey(key)
        return self._opts.get(key, None)

    # region quality of life

    def modelId(self) -> str:
        return self._opts["pid"]

    def task(self) -> typing.Callable[[...], typing.Any]:
        return self._opts.get("task", lambda _=None: None)

    def onStart(self) -> typing.Callable[[...], typing.Any]:
        return self._opts.get("on_start", lambda _=None: None)

    def onError(self) -> typing.Callable[[...], typing.Any]:
        return self._opts.get("on_error", lambda _=None: None)

    def onSuccess(self) -> typing.Callable[[...], typing.Any]:
        return self._opts.get("on_success", lambda _=None: None)

    def taskParams(self) -> typing.Any:
        return self._opts.get("task_params")

    def taskResults(self) -> typing.Any:
        return self._opts.get("task_results")

    def taskError(self) -> Exception | None:
        return self._opts.get("task_error", None)

    # endregion

    # endregion

    # region helpers

    def __validateKey(self, key: str):
        if key not in self.accepted_keys:
            raise ValueError("Invalid keyword argument: {}, accepted keywords: {}".format(key, ", ".join(self.accepted_keys)))

    # endregion

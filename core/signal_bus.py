import PySide6.QtCore as qtc


class SignalBus(qtc.QObject):
    launchThread = qtc.Signal(object)
    terminateThread = qtc.Signal(str)
    stopThread = qtc.Signal(str)
    CopyToClipboard = qtc.Signal(object)


signalBus = SignalBus()
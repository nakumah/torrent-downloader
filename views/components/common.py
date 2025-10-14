import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg


class QColoredLabel(qtw.QLabel):
    def __init__(self, color: qtg.QColor | str, **kwargs):
        super().__init__(**kwargs)

        palette = self.palette()

        palette.setColor(qtg.QPalette.ColorRole.WindowText, color)
        self.setPalette(palette)


class QWeightedColorLabel(QColoredLabel):
    def __init__(self, weight: qtg.QFont.Weight = qtg.QFont.Weight.Bold, **kwargs):
        super().__init__(**kwargs)

        font = self.font()
        font.setWeight(weight)

        self.setFont(font)

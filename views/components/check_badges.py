from typing import overload

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg

from resources.styling import loadStyle, parseStyle


class CheckBadge(qtw.QFrame):
    checkedChanged = qtc.Signal(tuple)

    def __init__(self, badgeId: str, label="", data=None, parent=None):
        super(CheckBadge, self).__init__(parent)

        self.__checkbox = qtw.QCheckBox(self)
        self.__label = qtw.QLabel(self)
        self.__label.setText(label)
        self.__data = data
        self.__badgeId = badgeId

        layout = qtw.QHBoxLayout()
        layout.addWidget(self.__checkbox)
        layout.addWidget(self.__label)
        layout.addStretch()

        self.setLayout(layout)

        self.setObjectName("CheckBadge")
        self.applyStyle()

        self.__configure()

    # region configure

    def __configure(self):
        self.__checkbox.checkStateChanged.connect(self.__handleCheckChanged)

    # endregion

    # region setters

    def setChecked(self, checked):
        self.__checkbox.setChecked(checked)

    def setLabel(self, label):
        self.__label.setText(label)

    def setData(self, data):
        self.__data = data

    # endregion

    # region getters
    def checkBox(self):
        return self.__checkbox

    def label(self):
        return self.__label

    def isChecked(self):
        return self.__checkbox.isChecked()

    def text(self):
        return self.__label

    def data(self):
        return self.__data

    def id(self):
        return self.__badgeId

    # endregion

    # region events handlers

    def __handleCheckChanged(self, state: qtg.Qt.CheckState):
        self.checkedChanged.emit((self.__badgeId, state))
        self.applyStyle()

    def mousePressEvent(self, event):
        if event.button() == qtg.Qt.MouseButton.LeftButton:
            self.setChecked(not self.__checkbox.isChecked())

    # endregion

    # region workers
    def applyStyle(self):
        style = loadStyle(":/qss/check_badge.qss")

        if self.isChecked():
            modifier = """\n
                QFrame#CheckBadge{
                    background: highlight_rgb;
                    border-radius: 10px;
                    border: 1px solid light_shade_rgb;
                }
            
                QFrame#CheckBadge QLabel{
                    color: light_rgb;
                    font-weight: 600;
                }
            """
            style += parseStyle(modifier)

        self.setStyleSheet(style)
    # endregion

    # region override

    def __str__(self):
        return f"CheckBadge: badgeId={self.__badgeId}"

    # endregion

class CheckBadgeGroup(qtw.QFrame):

    badgeCheckChanged = qtc.Signal(tuple)

    def __init__(self, parent=None):
        super(CheckBadgeGroup, self).__init__(parent)

        self.__kv: dict[str, CheckBadge] = {}

        self.contentLayout = qtw.QHBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        contentWidget = qtw.QWidget(self)
        contentWidget.setLayout(self.contentLayout)

        holderLayout = qtw.QHBoxLayout()
        holderLayout.setContentsMargins(0, 0, 0, 0)
        holderLayout.addWidget(contentWidget)
        holderLayout.addStretch()

        self.setLayout(holderLayout)

        self.setObjectName("CheckBadgeGroup")

    @overload
    def addBadge(self, badge: CheckBadge) -> str:
        ...

    @overload
    def addBadge(self, label: str = "", data=None, ) -> str:
        ...

    @overload
    def addBadge(self, badgeId: str=None, label: str = "", data=None, ) -> str:
        ...

    def addBadge(self, *args) -> str:
        if len(args) == 1:
            badge = args[0]
            assert isinstance(badge, CheckBadge), "Expected CheckBadge but got {}".format(type(args[0]))

            badge.checkedChanged.connect(lambda _: self.badgeCheckChanged.emit(badge))
            self.__kv[badge.id()] = badge

            return badge.id()

        elif len(args) == 2:
            bid = str(1 + self.contentLayout.count())

            assert isinstance(args[0], str)

            badge = CheckBadge(badgeId=bid, label=args[0], data=args[1], parent=self)
            badge.checkedChanged.connect(lambda _: self.badgeCheckChanged.emit(badge))
            self.contentLayout.addWidget(badge)
            return bid

        elif len(args) == 3:
            assert isinstance(args[0], str), "Expected a string as badgeId, but got {}".format(type(args[0]))
            assert len(args[0]) > 0, "BadgeId must be at least 1 character, but got {}".format(len(args[0]))

            assert isinstance(args[1], str), "Expected a string as label, but got {}".format(type(args[1]))

            badge = CheckBadge(badgeId=args[0], label=args[1], data=args[2], parent=self)
            self.contentLayout.addWidget(badge)
            return args[0]
        else:
            raise TypeError("addBadge takes exactly 3 arguments")

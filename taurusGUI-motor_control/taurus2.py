#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tango

from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel

from taurus.qt.qtgui.base import TaurusBaseWritableWidget
from taurus.core.taurusbasetypes import TaurusEventType

class MyTaurusEdit(Qt.QLineEdit, TaurusBaseWritableWidget):
    def __init__(self, qt_parent=None, designMode=False):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QLineEdit, qt_parent)
        self.call__init__(TaurusBaseWritableWidget, name, designMode=designMode)

        self.numberChanged.connect(self.notifyValueChanged)
        self.returnPressed.connect(self.writeValue)
        self.valueChangedSignal.connect(self.updatePendingOperations)
        self._configured = False

    def handleEvent(self, evt_src, evt_type, evt_value):
        if evt_type == TaurusEventType.Config or not self._configured:
            if evt_value is not None:
                obj = self.getModelObj()
                # set decimal digits
                self.setDigitCount(int_nb=None, dec_nb=obj.precision)
                # set min and max values
                min_, max_ = obj.getRange()
                if min_ is not None:
                    self.setMinValue(min_.magnitude)
                if max_ is not None:
                    self.setMaxValue(max_.magnitude)
                self._configured = True

        TaurusBaseWritableWidget.handleEvent(
            self, evt_src, evt_type, evt_value)


    model = Qt.pyqtProperty("QString", TaurusBaseWritableWidget.getModel,
                            TaurusBaseWritableWidget.setModel,
                            TaurusBaseWritableWidget.resetModel)

    useParentModel = Qt.pyqtProperty("bool", TaurusBaseWritableWidget.getUseParentModel,
                                     TaurusBaseWritableWidget.setUseParentModel,
                                     TaurusBaseWritableWidget.resetUseParentModel)

    autoApply = Qt.pyqtProperty("bool", TaurusBaseWritableWidget.getAutoApply,
                                TaurusBaseWritableWidget.setAutoApply,
                                TaurusBaseWritableWidget.resetAutoApply)

    forcedApply = Qt.pyqtProperty("bool", TaurusBaseWritableWidget.getForcedApply,
                                  TaurusBaseWritableWidget.setForcedApply,
                                  TaurusBaseWritableWidget.resetForcedApply)

class Widget(Qt.QWidget):

    def __init__(self):
        Qt.QWidget.__init__(self)
        self.setWindowTitle('Motor Control Center')
        self.setGeometry(1000,300,800,350)
        self.setMinimumSize(300,200)

        self.__step = 1
        self.__pos = 0

        self.__dev = tango.DeviceProxy('tau/dummies/1')
        self.__dev.pos = self.__pos

        self.window_setup()

    # unten in der Leiste
    def setIcon(self):
        icon1 = Qt.QIcon('actions:player_play.svg')
        self.setWindowIcon(icon1)

    # action of button above
    def quexit(self):
        app.quit()

    def moveR(self):
        self.__pos += self.__step
        self.__dev.pos = self.__pos

    def moveL(self):
        self.__pos -= self.__step
        self.__dev.pos = self.__pos

    def window_setup(self):
        #self.hboxGen()

        vbox = Qt.QVBoxLayout()
        self.mots = 2 # enter number of attributes/mots on display
        self.stepline = []
        self.posline = []
        self.c = 0
        self.dic = {}
        self.dic2 = {}

        for i in range(self.mots):
            self.dic[i]=Qt.QLineEdit(self)
            self.dic[i].move(0,-50)
            self.dic2[i]=Qt.QLineEdit(self)
            self.dic2[i].move(0,-50)

        A = self.motorHBox('tau/dummies/1', 'pos', 0) # add motors and info
        B = self.motorHBox('tau/dummies/1', 'temperature', 1)
        #C = self.motorHBox('again some motor', 'hum')

        self.vboxAssembly(A, B) # add motors you need

        vbox.addWidget(self.groupBoxMot)
        #vbox.addWidget(self.groupBoxGen)
        self.setLayout(vbox)
        Qt.QToolTip.setFont(Qt.QFont('Decorative', 10, Qt.QFont.Bold))


    # general info
    def hboxGen(self):
        self.groupBoxGen = Qt.QGroupBox('Allgemeines')

        hbox = Qt.QHBoxLayout()

        #quitbtn = self.setButton()
        #hbox.addWidget(quitbtn)

        self.groupBoxGen.setLayout(hbox)

    # given a motor and the attribute (both string) will construct a stepper
    def motorHBox(self, motor, attr, num):
        stepline = self.dic.get(num)
        posline = self.dic2.get(num)
        # following is the construction of a hor. motor block,
        # to be contained in self.groupBox2_1 (as in first line of the second box)
        self.groupBox2_1 = Qt.QGroupBox(motor + '/' + attr)
        self.groupBox2_1.setMaximumHeight(90)

        hbox = Qt.QHBoxLayout()

        stepline.setPlaceholderText('Schrittweite')
        stepline.setMinimumHeight(40)
        stepline.setMaximumWidth(150)
        stepline.returnPressed.connect(lambda: self.stepButton(num))
        hbox.addWidget(stepline)

        posline.setPlaceholderText('Zielposition')
        posline.returnPressed.connect(lambda: self.newPos(num))
        posline.setMinimumHeight(40)
        posline.setMaximumWidth(150)
        posline.setMaxLength(80)
        hbox.addWidget(posline)

        hbox.addStretch()

        buttonLL = Qt.QPushButton(Qt.QIcon('actions:go-backward.svg'), '', self)
        buttonLL.setMinimumHeight(40)
        buttonLL.setMinimumWidth(60)
        hbox.addWidget(buttonLL)

        buttonL = Qt.QPushButton(Qt.QIcon('actions:left.svg'), '', self)
        buttonL.clicked.connect(self.moveL)
        buttonL.setMinimumHeight(40)
        buttonL.setMinimumWidth(60)
        hbox.addWidget(buttonL)

        w = MyTaurusEdit()
        w.setMaximumHeight(40)
        w.setMinimumWidth(80)
        hbox.addWidget(w)
        w.model = motor + '/' + attr

        buttonR = Qt.QPushButton(Qt.QIcon('actions:right.svg'), '', self)
        buttonR.clicked.connect(self.moveR)
        buttonR.setMinimumHeight(40)
        buttonR.setMinimumWidth(60)
        hbox.addWidget(buttonR)

        buttonRR = Qt.QPushButton(Qt.QIcon('actions:go-forward.svg'), '', self)
        buttonRR.setMinimumHeight(40)
        buttonRR.setMinimumWidth(60)
        hbox.addWidget(buttonRR)

        self.groupBox2_1.setLayout(hbox)
        #self.c += 1

        return self.groupBox2_1

    def stepButton(self, num):
        stepline = self.dic.get(num)

        self.__step = float(stepline.text())

    def newPos(self, num):
        posline = self.dic2.get(num)

        self.__pos = float(posline.text())
        self.__dev.pos = self.__pos

    def vboxAssembly(self, *groups):
        self.groupBoxMot = Qt.QGroupBox('Motors')

        vbox = Qt.QVBoxLayout()

        for i in groups:
            vbox.addWidget(i)

        self.groupBoxMot.setLayout(vbox)

if __name__ == "__main__":
    import sys
    app = TaurusApplication(cmd_line_parser=None)
    gui = Widget()
    gui.show()
    sys.exit(app.exec_())
    
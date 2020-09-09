#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tango

from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel


class Widget(Qt.QWidget):

    def __init__(self):
        Qt.QWidget.__init__(self)
        self.setWindowTitle('Motor Control Center')
        self.setGeometry(1000, 300, 800, 350)
        self.setMinimumSize(300, 200)

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
            self.dic[i].move(0, -50)
            self.dic2[i]=Qt.QLineEdit(self)
            self.dic2[i].move(0, -50)

            # only modify inside the box below
###########################################################################
        # add motors needed, followed by enumeration
        A = self.motorHBox('tau/dummies/1/pos', 0) # add motors and info
        B = self.motorHBox('tau/dummies/1/humidity', 1)

        self.vboxAssembly(A, B) # add motors you need assembled

###########################################################################
            # only modify in the box above

        vbox.addWidget(self.groupBoxMot)
        #vbox.addWidget(self.groupBoxGen)
        self.setLayout(vbox)
        Qt.QToolTip.setFont(Qt.QFont('Decorative', 10, Qt.QFont.Bold))


    # general info
    def hboxGen(self):
        self.groupBoxGen = Qt.QGroupBox('Allgemeines')

        hbox = Qt.QHBoxLayout()

        self.groupBoxGen.setLayout(hbox)

    # given a motor and the attribute (both string) will construct a stepper
    def motorHBox(self, motor, num):
        stepline = self.dic.get(num)
        posline = self.dic2.get(num)
        # following is the construction of a hor. motor block,
        # to be contained in self.groupBox2_1 (as in first line of the second box)
        self.groupBox2_1 = Qt.QGroupBox(motor)
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
        '''
        buttonLL = Qt.QPushButton(Qt.QIcon('actions:go-backward.svg'), '', self)
        buttonLL.setMinimumHeight(40)
        buttonLL.setMinimumWidth(60)
        hbox.addWidget(buttonLL)
        '''
        buttonL = Qt.QPushButton(Qt.QIcon('actions:left.svg'), '', self)
        buttonL.clicked.connect(self.moveL)
        buttonL.setMinimumHeight(40)
        buttonL.setMinimumWidth(60)
        hbox.addWidget(buttonL)

        w = TaurusLabel()
        w.setMaximumHeight(40)
        w.setMinimumWidth(80)
        hbox.addWidget(w)
        w.model = motor

        buttonR = Qt.QPushButton(Qt.QIcon('actions:right.svg'), '', self)
        buttonR.clicked.connect(self.moveR)
        buttonR.setMinimumHeight(40)
        buttonR.setMinimumWidth(60)
        hbox.addWidget(buttonR)
        '''
        buttonRR = Qt.QPushButton(Qt.QIcon('actions:go-forward.svg'), '', self)
        buttonRR.setMinimumHeight(40)
        buttonRR.setMinimumWidth(60)
        hbox.addWidget(buttonRR)
        '''
        self.groupBox2_1.setLayout(hbox)
        #self.c += 1

        return self.groupBox2_1

    def stepButton(self, num):
        stepline = self.dic.get(num)
        try:
            self.__step = float(stepline.text())
        except:
            pass

    def newPos(self, num):
        posline = self.dic2.get(num)

        try:
            self.__pos = float(posline.text())
            self.__dev.pos = self.__pos
        except:
            pass

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
    

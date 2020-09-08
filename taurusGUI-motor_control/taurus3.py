#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tango

from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel

class MyGUI(Qt.QMainWindow):
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)
        self.setWindowTitle('Positions') # self stands for QMainWindow

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')

        

class Widget(Qt.QWidget):

    def __init__(self):
        Qt.QWidget.__init__(self)
        self.setWindowTitle('Motor Control Center')
        self.setGeometry(1000,300,800,350)
        self.setMinimumSize(300,200)

        self.__step = 1
        self.__pos = 0
        
        self.__dev = tango.DeviceProxy('tau/dummies/1')
        self.__dev. pos = self.__pos

        self.window_setup()

    # unten in der Leiste
    def setIcon(self):
        icon1 = Qt.QIcon('actions:player_play.svg')
        self.setWindowIcon(icon1)

    # pushable button and reaction
    '''
    def setButton(self):
        btn1 = Qt.QPushButton('Quit', self)
        btn1.move(400,300)
        btn1.setMaximumWidth(100)
        btn1.setMinimumHeight(50)
        btn1.clicked.connect(self.quexit)
        return btn1
    '''

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

        A = self.motorHBox('tau/dummies/1', 'pos')
        B = self.motorHBox('tau/dummies/1', 'temperature')
        C = self.motorHBox('again some motor', 'hum')

        self.vboxAssembly(A, B, C)

        vbox.addWidget(self.groupBoxMot)
        #vbox.addWidget(self.groupBoxGen)
        self.setLayout(vbox)

        Qt.QToolTip.setFont(Qt.QFont('Decorative', 10, Qt.QFont.Bold))

    def stepButton(self):
        if self.stepline.text() == '':
            return
        print(type(self.stepline.text()), float(self.stepline.text()))
        self.__step = float(self.stepline.text())

    def newPos(self):
        self.__pos = float(self.posline.text())
        self.__dev.pos = self.__pos

    # general info
    def hboxGen(self):
        self.groupBoxGen = Qt.QGroupBox('Allgemeines')

        hbox = Qt.QHBoxLayout()

        #quitbtn = self.setButton()
        #hbox.addWidget(quitbtn)

        self.groupBoxGen.setLayout(hbox)

    # given a motor and the attribute (both string) will construct a stepper
    def motorHBox(self, motor, attr):
        # following is the construction of a hor. motor block,
        # to be contained in self.groupBox2_1 (as in first line of the second box)
        self.groupBox2_1 = Qt.QGroupBox(motor + '/' + attr)
        self.groupBox2_1.setMaximumHeight(90)

        hbox = Qt.QHBoxLayout()

        self.stepline = Qt.QLineEdit(self)
        self.stepline.setPlaceholderText('Schrittweite')
        self.stepline.setMinimumHeight(40)
        self.stepline.setMaximumWidth(150)
        hbox.addWidget(self.stepline)

        btn_step = Qt.QPushButton(Qt.QIcon('actions:go-jump.svg'), '', self)
        btn_step.clicked.connect(self.stepButton)
        btn_step.setMinimumHeight(40)
        btn_step.setMinimumWidth(60)
        hbox.addWidget(btn_step)

        self.posline = Qt.QLineEdit(self)
        self.posline.setPlaceholderText('Zielposition')
        self.posline.setMinimumHeight(40)
        self.posline.setMaximumWidth(150)
        self.posline.setMaxLength(80)
        hbox.addWidget(self.posline)

        btn_newpos = Qt.QPushButton(Qt.QIcon('actions:go-jump.svg'), '', self)
        btn_newpos.clicked.connect(self.newPos)
        btn_newpos.setMinimumHeight(40)
        btn_newpos.setMinimumWidth(60)
        hbox.addWidget(btn_newpos)

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

        w = TaurusLabel()
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

        return self.groupBox2_1

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
    '''
    layout = Qt.QHBoxLayout()
    w = TaurusLabel()
    layout.addWidget(w)
    w.model = 'test/dummies/1/pos'
    gui.setLayout(layout)
    '''
    gui.show()
    sys.exit(app.exec_())
    
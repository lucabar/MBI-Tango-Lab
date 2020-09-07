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
        self.setWindowTitle('Widget One')
        self.setGeometry(1200,300,500,400)
        self.setMinimumSize(300,200)

        self.__step = 3
        self.__pos = 0

        self.window_setup()

        #self.setIcon()
        #self.setIcon_modes()
        #self.setButton()
        #self.center()


    # unten in der Leiste
    def setIcon(self):
        icon1 = Qt.QIcon("categories:xfce-devel.svg")
        self.setWindowIcon(icon1)

    # pushable button and reaction
    def setButton(self):
        btn1 = Qt.QPushButton('Quit', self)
        btn1.move(400,300)
        btn1.clicked.connect(self.quexit)
        return btn1

    # action of button above
    def quexit(self):
        app.quit()

    def moveR(self):
        tango.DeviceProxy('tau/dummies/1').pos += self.__step

    def moveL(self):
        tango.DeviceProxy('tau/dummies/1').pos -= self.__step

    def window_setup(self):
        self.hbox2()
        buttonL, buttonR = self.hbox1()

        vbox = Qt.QVBoxLayout()
        
        vbox.addWidget(self.groupBox2)
        vbox.addWidget(self.groupBox1)
        self.setLayout(vbox)

        Qt.QToolTip.setFont(Qt.QFont('Decorative', 10, Qt.QFont.Bold))
        #self.setToolTip('Our Main Window')

        buttonL.clicked.connect(self.moveL)
        buttonR.clicked.connect(self.moveR)

    def hbox1(self):
        self.groupBox1 = Qt.QGroupBox('Motor 1')

        hbox = Qt.QHBoxLayout()

        buttonLL = Qt.QPushButton(Qt.QIcon('actions:go-backward.svg'), '', self)
        buttonLL.setMinimumHeight(40)
        hbox.addWidget(buttonLL)

        buttonL = Qt.QPushButton(Qt.QIcon('actions:left.svg'), '', self)
        buttonL.setMinimumHeight(40)
        hbox.addWidget(buttonL)

        
        w = TaurusLabel()
        w.setMaximumHeight(40)
        hbox.addWidget(w)
        w.model = 'tau/dummies/1' + '/pos'

        buttonR = Qt.QPushButton(Qt.QIcon('actions:right.svg'), '', self)
        buttonR.clicked.connect(self.moveR)
        buttonR.setMinimumHeight(40)
        hbox.addWidget(buttonR)

        buttonRR = Qt.QPushButton(Qt.QIcon('actions:go-forward.svg'), '', self)
        buttonRR.setMinimumHeight(40)
        hbox.addWidget(buttonRR)

        self.groupBox1.setLayout(hbox)
        
        return buttonL, buttonR

    def hbox2(self):
        self.groupBox2 = Qt.QGroupBox('Allgemeines')

        hbox = Qt.QHBoxLayout()
        

        line1 = Qt.QLineEdit(self)
        line1.setPlaceholderText('Schrittweite')

        hbox.addWidget(line1)
        
        line2 = Qt.QLineEdit(self)
        line2.setPlaceholderText('Zielposition')
        hbox.addWidget(line2)

        btn1 = self.setButton()
        hbox.addWidget(btn1)

        
        self.groupBox2.setLayout(hbox)

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
    
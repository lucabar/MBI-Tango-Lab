#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020  MBI-Division-B
# MIT License, refer to LICENSE file
# Author: Luca Barbera / Email: barbera@mbi-berlin.de

import tango

from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel


class MotorWidget(Qt.QWidget):
    ''' This is not the tidiest Qt-code but it does the job. Most of this
    could have been done by OOP, but this was quicker.

    If more (or less) than two motors are chosen, the other need to be added
    to the enumeration A, B, ... below. Both editable sections are *** labeled

    Step sizes have to be floats greater than zero; jump position is float

    To add this MotorWidget in a TaurusGui:
        - choose "New panel"
        - set a Panel Name
        - click on "Other..."
        - set "motor_control" (name of this file) as "Module"
        - make sure the gui can access this file (e.g. copy into python-files or same directory)
        - select "MotorWidget" (name of this class) from Class dropdown
        - "Finish"
        - (optional) switch temporary status to permanent
    
    Important! After changing this file Panel must be re-added to the GUI !
    '''

    def __init__(self):
        Qt.QWidget.__init__(self)
        self.setWindowTitle('Motor Control Center')
        self.setGeometry(1000, 300, 500, 350)
        self.setMinimumSize(300, 200)

        self.__step = 1 # default stepsize
        self.__pos = 0 # default jump position
        

        # initialize contact to the device whose attributes will be accessed
        # this part should be updated by a faster/cleaner method
        self.deviceproxydict = {} # dict that stores the devices
        self.attributedict = {} # dict that stores the attributes

        self.steplinedict = {} # dict that stores the QLineEdit for step size
        self.poslinedict = {} # dict that stores the QLineEdit for jump pos
        self.stepdict = {} # dict that stores step size for each motor

# edit only below; add new motor+attribute
# ************************************************************************ #

        self.devices = ['tau/dummies/1', 'tau/dummies/1']
        attributes = ['pos','temperature']

# ************************************************************************ #
# edit only above

        if len(self.devices) == len(attributes):
            self.mots = len(attributes)
        else:
            raise Exception('The amount of devices does not match the amount of attributes!')

        c = 0
        for dev in self.devices:
            self.deviceproxydict[c] = tango.DeviceProxy(dev)
            self.attributedict[c] = attributes[c]
            c += 1

        self.window_setup()

    def moveR(self, num):
        step = self.stepdict.get(num)
        dev = self.deviceproxydict.get(num)
        attr = self.attributedict.get(num)
        dev[attr] = dev[attr].value + step

    def moveL(self, num):
        step = self.stepdict.get(num)
        dev = self.deviceproxydict.get(num)
        attr = self.attributedict.get(num)
        dev[attr] = dev[attr].value - step

    def window_setup(self):
        vbox = Qt.QVBoxLayout()

        for i in range(self.mots):
            self.steplinedict[i]=Qt.QLineEdit(self)
            self.steplinedict[i].move(0, -50) 
            self.poslinedict[i]=Qt.QLineEdit(self)
            self.poslinedict[i].move(0, -50)
            self.stepdict[i] = 1

# edit only below
# ************************************************************************ #
        
        # enter entire attributes needed and enumeration A = 0, B = 1, etc.
        # has to be the same as motor and attr in the dicts in init
        A = self.motorHBox(str(self.devices[0]+'/'+self.attributedict[0]), 0)
        B = self.motorHBox(str(self.devices[1]+'/'+self.attributedict[1]), 1)

        self.vboxAssembly(A, B) # add motors you need assembled

# ************************************************************************ #
# edit only above

        vbox.addWidget(self.groupBoxMot)
        #vbox.addWidget(self.groupBoxGen)
        self.setLayout(vbox)
        Qt.QToolTip.setFont(Qt.QFont('Decorative', 10, Qt.QFont.Bold))

    # given a motor and the attribute (both string) will construct a stepper
    def motorHBox(self, motor, num):
        # one dict for the step size, one for the jump position
        stepline = self.steplinedict.get(num)
        posline = self.poslinedict.get(num)
        
        # following is the construction of a hor. motor block,
        # to be contained in self.groupBox2_1 (first line of the second box)
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
        this button could be used for a "jog"-function. just click.connect it
        to the function needed
        buttonLL = Qt.QPushButton(Qt.QIcon('actions:go-backward.svg'), '', self)
        buttonLL.setMinimumHeight(40)
        buttonLL.setMinimumWidth(60)
        hbox.addWidget(buttonLL)
        '''
        buttonL = Qt.QPushButton(Qt.QIcon('actions:left.svg'), '', self)
        buttonL.clicked.connect(lambda: self.moveL(num))
        buttonL.setMinimumHeight(40)
        buttonL.setMinimumWidth(60)
        hbox.addWidget(buttonL)

        w = TaurusLabel()
        w.setMaximumHeight(40)
        w.setMinimumWidth(80)
        hbox.addWidget(w)
        w.model = motor

        buttonR = Qt.QPushButton(Qt.QIcon('actions:right.svg'), '', self)
        buttonR.clicked.connect(lambda: self.moveR(num))
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

        return self.groupBox2_1

    def stepButton(self, num):
        stepline = self.steplinedict.get(num)
        try:
            if float(stepline.text()) > 0:
                self.stepdict[num] = float(stepline.text())
        except:
            pass

    def newPos(self, num):
        posline = self.poslinedict.get(num)
        dev = self.deviceproxydict.get(num)
        attr = self.attributedict.get(num)
        try:
            position = float(posline.text())
            dev[attr] = position
        except:
            pass

    def vboxAssembly(self, *groups):
        # this takes all the motor hboxes and assembles them into one widget
        self.groupBoxMot = Qt.QGroupBox('Motors')

        vbox = Qt.QVBoxLayout()

        for box in groups:
            vbox.addWidget(box)

        self.groupBoxMot.setLayout(vbox)

if __name__ == "__main__":
    import sys
    app = TaurusApplication(cmd_line_parser=None)
    gui = MotorWidget()
    gui.show()
    sys.exit(app.exec_())
    

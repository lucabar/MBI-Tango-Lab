#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:14:58 2020

@author: lucajul
"""

from taurus.qt.qtgui.taurusgui.utils import PanelDescription,\
    ExternalApp, ToolBarDescription, AppletDescription

from taurus.qt.qtgui.panel.taurusform import TaurusForm
from taurus2 import Widget


GUI_NAME = 'heartbeatform'
ORGANIZATION = 'DESY'


if __name__ == '__main__':
    from taurus.qt.qtgui.application import TaurusApplication
    from taurus.qt.qtgui.taurusgui import TaurusGui
    from taurus.external.qt import Qt
    app = TaurusApplication()
    gui = TaurusGui()

    gui.loadConfiguration(__file__)
    panel = Widget()
    gui.createPanel(panel, 'yoo')
    gui.show()
    app.exec_()
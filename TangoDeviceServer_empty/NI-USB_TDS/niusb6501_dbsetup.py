#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''this script registers the Tango Device Server for the NI-USB6501 under the
instance name -sys-. Run this script to automatically register with the Tango database.'''

import tango

dev_info = tango.DbDevInfo()
dev_info.server = "NIUSB6501/sys"
dev_info._class = "NIUSB6501"
dev_info.name = "sys/ni_usb_TDS/1"

db = tango.Database()
db.add_device(dev_info)

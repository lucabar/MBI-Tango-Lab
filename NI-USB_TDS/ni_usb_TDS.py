#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:17:29 2020

@author: Luca Barbera

Integers 0-63 (both included) are equivalent to the logical 0, 
    while int 64-127 are equivalent to logical 1.
Integers above 127 or below 0 raise errors.
When reading port it will return 1 for open and 0 for closed.
Ports must be 0,1,2 and values same as the logicals explained above.
"""
from tango import AttrWriteType, DevState, DebugIt
from tango.server import Device, attribute, command

import ni_usb_6501 as ni

class NIUSB6501(Device):
    
    line = attribute(name='Line', access = AttrWriteType.READ_WRITE,
                     description = 'Contains information of whether line is open or closed',
                     fget='get_line',fset='set_line')
    
    
    def init_device(self):
        self.info_stream('Trying to establish connection')
        
        try:
            Device.init_device(self)
            self.dev = ni.get_adapter()
            self.set_state(DevState.ON)
            self.dev.set_io_mode(0,127,0)#sets port0 and port2 to "read" i.e. "not writable.
            self.dev.write_port(1,0)
            #print(self.dev.read_port(1))
            self.__line = 0
            self.info_stream('Connection established.')
        except:
            if not self.dev:
                self.error_stream('Connection could not be established')
                self.set_state(DevState.FAULT)
            else:
                self.info_stream('Connection has already been established in a prior run.')
            
    @DebugIt
    def read_line(self):
        port = 1
        #defaut is port 1 (lines 3-6 and 27-30)
        #method only returns 0,1 (off,on) for the entire port (i.e. 8 IO lines)
        try:
            val = self.dev.read_port(port)
            if val < 192 and val >= 0:
                self.debug_stream('Port {}'.format(port),'is off.')
                self.__line = 0
            elif val < 256 and val >191:
                self.debug_stream('Port {}'.format(port),'is on.')
                self.__line = 1
            else:
                self.error_stream(val,type(val))
            
        except:
            self.error_stream('No permission to read port. Should check initially declared I/O mode.')  
                              
    def get_line(self):
        return self.__line 
    
    def set_line(self,value):
        self.write_line(value)
        self.__line = value
        
                            
    @DebugIt()
    def write_line(self,value):
        port = 1
        #writes entire port to 0,1 (off, on), i.e. all containing 8 IO lines
        try:
            if value == 0:
                self.dev.write_port(port,0)
                self.debug_stream('Port {}'.format(port),' is now off.')
                self.__line = 0
            elif value == 1:
                self.dev.write_port(port,127)
                self.debug_stream('Set port {}'.format(port),'is now on.')
                self.__line = 1
            else:
                self.error_stream('Value not valid. Use 0 = closed, 1 = open.')
                
        except:
            self.error_stream('No permission to write port. Should check initially declared I/O mode.')
            
        
if __name__ == "__main__":
    NIUSB6501.run_server()
            

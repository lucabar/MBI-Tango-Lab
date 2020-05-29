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
                     fget='get_line',fset='set_line', max_value=1,min_value=0,
                     doc='state of all the lines under port 1',dtype=int)
    
    port = attribute(name='Active Port',
                            doc='contains the number of port (0,1,2) that is being used',
                            access=AttrWriteType.READ_WRITE,max_value=2,min_value=0,
                            dtype=int,fget='get_port',fset='set_port')
    
    def init_device(self):
        self.info_stream('Trying to establish connection')
        #initiation sets port to 1, line to 0 (closed) and makes port 1 writeable
        # and ports 0,2 readable (not writeable)
        
        try:
            Device.init_device(self)
            self.dev = ni.get_adapter()
            self.set_state(DevState.ON)
            self.dev.set_io_mode(0,127,0)#sets port0 and port2 to "read" i.e. "not writable.
            self.__port = 1
            self.__line = 0
            self.dev.write_port(self.__port,0)

            self.info_stream('Connection established.')
            
        except:
            if not self.dev:
                self.error_stream('Connection could not be established')
                self.set_state(DevState.FAULT)
            else:
                #Connection already running (info_stream gets called in case
                #the init method is called more than once)
                self.info_stream('Connection has already been established in a prior run.')
            
    
    def get_line(self):
        return self.__line 
    
    def set_line(self,value):
        self.write_line(value)
        self.__line = value
        
    @DebugIt
    def read_line(self):
        #defaut is port 1 (lines 3-6 and 27-30)
        #method only returns 0,1 (off,on) for the entire port (i.e. 8 IO lines)
        try:
            val = self.dev.read_port(self.__port)
            if val < 192 and val >= 0:
                self.debug_stream('Port {}'.format(self.__port),'is off.')
                self.__line = 0
            elif val < 256 and val >191:
                self.debug_stream('Port {}'.format(self.__port),'is on.')
                self.__line = 1
            
        except:
            self.error_stream('No permission to read port. Should check initially declared I/O mode.')  
    
                            
    @DebugIt()
    def write_line(self,value):
        #writes entire port to 0,1 (off, on), i.e. all containing 8 IO lines
        self.__line = value
        try:
            if self.__line == 0:
                self.dev.write_port(self.__port,0)
                self.debug_stream('Port {}'.format(self.__port),' is now off.')
            elif self.__line == 1:
                self.dev.write_port(self.__port,127)
                self.debug_stream('Set port {}'.format(self.__port),'is now on.')
            else:
                self.error_stream('Value not valid. Use 0 = closed, 1 = open.')
                
        except:
            self.error_stream('No permission to write port. Should check initially declared I/O mode.')
    
    def get_port(self):
        return self.__port
    
    def set_port(self,number):
        self.change_port(number)
        
    @DebugIt
    def change_port(self,number):
        self.__port = number
        if self.__port == 0:
            self.dev.set_io_mode(127,0,0)
        elif self.__port == 1:
            self.dev.set_io_mode(0,127,0)
        elif self.__port == 2:
            self.dev.set_io_mode(0,0,127)
        
        
        
if __name__ == "__main__":
    NIUSB6501.run_server()
            

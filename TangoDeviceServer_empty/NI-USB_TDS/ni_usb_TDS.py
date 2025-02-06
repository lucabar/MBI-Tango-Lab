#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:17:29 2020

@author: Luca Barbera



"""
from tango import AttrWriteType, DevState, DebugIt
from tango.server import Device, attribute, command
import time
import ni_usb_6501 as ni


class NIUSB6501(Device):
    
    
    port3 = attribute(fget='read_port3',fset='write_port3',name='Port_1.3',access=AttrWriteType.READ_WRITE,dtype=bool)
    
    port4 = attribute(fget='read_port4',fset='write_port4',name='Port_1.4',access=AttrWriteType.READ_WRITE,dtype=bool)
    
    port5 = attribute(fget='read_port5',fset='write_port5',name='Port_1.5',access=AttrWriteType.READ_WRITE,dtype=bool)
    
    port6 = attribute(fget='read_port6',fset='write_port6',name='Port_1.6',access=AttrWriteType.READ_WRITE,dtype=bool)
    
    port7 = attribute(fget='read_port7',fset='write_port7',name='Port_1.7',access=AttrWriteType.READ_WRITE,dtype=bool)
    
    gatetime = attribute(fget='read_gatetime',fset='write_gatetime',name='Gatetime',access=AttrWriteType.READ_WRITE,dtype=float,min_value=0)
    
    act_port = attribute(fget='read_act_port',fset='write_act_port',name='ActivePort',access=AttrWriteType.READ_WRITE,dtype=int,min_warning=2, min_value=0,max_value=7)
    
    frequency = attribute(fget='read_frequency',fset='write_frequency',name='Frequency',access=AttrWriteType.READ_WRITE,dtype=float,min_value=1)
    
    def init_device(self):
        self.info_stream('Trying to establish connection')
        
        try:
            Device.init_device(self)
            self.dev = ni.get_adapter()
            self.set_state(DevState.ON)
            self.dev.set_io_mode(0b00000000,0b01111111,0b00000000) #only ports 1.0-1.7 are writeable
            self.__ports = {3:False,4:False,5:False,6:False,7:False}
            self.__active = '0b00000000'
            self.dev.write_port(1,int(self.__active,2))
            self.info_stream('Connection established.')
            
            self.__gatetime = 1
            self.__act_port = 3
            self.__freq = 1
            
        except:
            if not self.dev:
                self.error_stream('Connection could not be established')
                self.set_state(DevState.FAULT)
            else:
                #Connection already running (info_stream gets called in case
                #the init method is called more than once)
                self.info_stream('Connection has already been established in a prior run.')
                
        
    def read_port3(self):
        return self.__ports[3]
    
    def write_port3(self,state):
        self.change_port(3,state)
    
    def read_port4(self):
        return self.__ports[4]
    
    def write_port4(self,state):
        self.change_port(4,state)
    
    def read_port5(self):
        return self.__ports[5]
    
    def write_port5(self,state):
        self.change_port(5,state)
    
    def read_port6(self):
        return self.__ports[6]
    
    def write_port6(self,state):
        self.change_port(6,state)
    
    def read_port7(self):
        return self.__ports[7]
    
    def write_port7(self,state):
        self.change_port(7,state)
        
        
    def read_gatetime(self):
        return self.__gatetime
    
    def write_gatetime(self,value):
        self.__gatetime = value
        
    def read_act_port(self):
        return self.__act_port
    
    def write_act_port(self,value):
        self.__act_port = value
    
    def read_frequency(self):
        return self.__freq
    
    def write_frequency(self,value):
        self.__freq = value
    
    @DebugIt(show_args=True,show_ret=True)
    def change_active(self,port,state):
        new = -1-port
        self.__active=list(self.__active)
        
        if state:    
            self.__active[new] = '1'
        if not state:
            self.__active[new] = '0'
        self.__active = ''.join(self.__active)
        bitmap = self.__active
        return bitmap
    
    @DebugIt()            
    def change_port(self, port, state):
        self.change_active(port,state)
        self.dev.write_port(1,int(self.__active,2))
        self.__ports[port] = state
        self.debug_stream('changed port'+str(port)+' to '+str(state))
    #using the gate_timer for longer than 3s command will create a timeout error
    #the command will still be executed as desired, but a warning will be sent
    @DebugIt()
    @command()    
    def gate_timer(self):
        start = time.time()
        self.change_port(self.__act_port,True)
        self.info_stream('Port{} active'.format(self.__act_port))
        time.sleep(self.__gatetime)
        self.change_port(self.__act_port,False)
        self.info_stream('Port{} inactive'.format(self.__act_port))
        self.debug_stream('Actual duration of gate: '+ str(time.time()-start))

    #The frequency of the pulsetrain is not correct (as one can see by the "hits" in debug-mode).
    @DebugIt()
    @command()
    def pulsetrain(self):
        hits = 0

        bitmap_on = int(self.change_active(self.__act_port,True),2)
        bitmap_off = int(self.change_active(self.__act_port,False),2)
        self.debug_stream(str(bitmap_on))
        self.debug_stream(str(bitmap_off))
        
        start = time.time()
        while time.time() <= start+self.__gatetime:
            hits += 1
            self.dev.write_port(1,bitmap_on)
            time.sleep(1/(self.__freq))
            self.dev.write_port(1,bitmap_off)
            time.sleep(1/(self.__freq))
        act_dur = time.time()-start
        self.debug_stream('Actual duration:'+str(act_dur))
        self.debug_stream('Actual hits: '+str(hits))
    
            
        
if __name__ == "__main__":
    NIUSB6501.run_server()
            


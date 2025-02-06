#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    temperature and humidity measurement Tango Device Server
    
    Created on Wed Apr 22 15:19:58 2020
    @author: mbi
"""
import numpy
from tango import AttrWriteType, DevState, DebugIt, ErrorIt, InfoIt
from tango.server import Device, attribute, command
import AM2315 as am_driver


class TempHumid(Device):

    temperature = attribute(name='Temperature',access=AttrWriteType.READ,
                            dtype=float,fget='get_temperature',format='.2f',
                            min_value=-273.15,doc='the measured temperature',unit='C')

    humidity = attribute(name='Humidity',access=AttrWriteType.READ,dtype=float,fget='get_humidity',format='.2f',doc='the measured humidity',unit='%')

    def init_device(self):
        self.info_stream('Trying to connect device to server.')
        try:
            Device.init_device(self)
            self.am2315 = am_driver.AM2315()
            self.set_state(DevState.ON)
            self.temp = 0
            self.humid = 0
            self.info_stream("Connection established.")
        except:
            self.error_stream('Connection could not be established.')

    @DebugIt()
    @command()
    def get_data(self):
        try:
            #_read_data measures both humidity and temperature
            self.am2315._read_data()
            self.temp = self.am2315.temperature
            self.humid = self.am2315.humidity
        except:
            self.error_stream('Data could not be read')
    @InfoIt(show_ret=True)
    def get_temperature(self):
        return self.temp

    @InfoIt(show_ret=True)
    def get_humidity(self):
        return self.humid
    
    @ErrorIt()
    @command()
    def error_func(self):
        print('You have made an error.')
        return None
    
    def read_state(self):
        return self.state()
if __name__ == "__main__":
    TempHumid.run_server()

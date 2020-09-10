#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright (C) 2020  MBI-Division-B
# MIT License, refer to LICENSE file
# Author: Luca Barbera / Email: barbera@mbi-berlin.de


from tango import AttrWriteType, DevState, DebugIt
from tango.server import Device, attribute, command, device_property

import visa

class LockInAmp(Device):
    '''
    pyvisa-py must be installed for this TDS to work.
    to talk to the device the "open_resource" command must be 
    string 'TCPIP::' followed by IP address of device inside string
    '''


# ------ Attributes ------ #

    X = attribute(label='X',
                         dtype=float,
                         access=AttrWriteType.READ,
                         doc='Readable X value.')

    Y = attribute(label='Y',
                         dtype=float,
                         access=AttrWriteType.READ,
                         doc='Readable Y value.')

    R = attribute(label='R',
                         dtype=float,
                         access=AttrWriteType.READ,
                         doc='Readable R value.')

    phase = attribute(name='phase',
                      label='Phase',
                      dtype=float,
                      access=AttrWriteType.READ,
                      doc='Readable phase attribute.')


# ------ Device Properties ------ #
    # device_properties will be set once per family-member and usually -
    # contain serial numbers or a certain port-ID that needs to be set once -
    # and will not change while the server is running.

    # enter IP-address to talk over TCP/IP via pyvisa
    port = device_property(dtype=int, default_value='192.168.1.242')

# ------ default functions that are inherited from parent "Device" ------ #
    def init_device(self):
        Device.init_device(self)
        self.info_stream('Connecting...')  # prints this line while -
        # in logging mode "info" or lower
        self.set_state(DevState.ON)

        rm = visa.ResourceManager('@py')
        self.inst = rm.open_resource('TCPIP::'+str(self.port))
        idn = self.inst.query('*IDN?')
        if idn:
            self.info_stream('Instrument ID: ' + idn)
            self.info_stream('Connection established!')
        else:
            self.info_stream('Instrument could not be initialized.')

        self.__X = 0
        self.__Y = 0
        self.__R = 0
        self.__phase = 0

    def delete_device(self):
        self.set_state(DevState.OFF)
        self.error_stream('A device was deleted!')  # prints this line while -
        # in logging mode "error" or lower.

    # define what is executed when Tango checks for the state.
    # Here you could inquire the state of the hardware and not just -
    # (as it is in default) of the TDS.
    # Default returns state but also sets state from ON to ALARM if -
    # some attribute alarm limits are surpassed.
    #def dev_state(self):
        # possible pseudo code:
        # if hardware-state and TDS-state is ON:
        #   return DevState.ON
        # else:
        #   return DevState.FAULT
        #return DevState
    '''
    def always_executed_hook(self):
        this does not need to implemented but could be used for polling
        one, two or three attributes continuously and at the same time instead of calling
        them each time they are read. can be used for phase as well
    
        self.__X, self.__Y, self.__R = self.inst.query('SNAP? X, Y, R')
    '''

# ------ Read/Write functions ------ #
    @DebugIt()
    def read_X(self):  # this is default to read humidity
        self.__X = float(self.inst.query('OUTP? X'))
        return self.__X

    @DebugIt()
    def read_Y(self):
        self.__Y = float(self.inst.query('OUTP? Y'))
        return self.__Y

    def read_R(self):
        self.__R = float(self.inst.query('OUTP? R'))
        return self.__R

    @DebugIt()
    def read_phase(self):
        self.__phase = float(self.inst.query('OUTP? TH'))
        return self.__phase

    # more examples of externally executable methods
    @command()
    def turn_off(self):
        self.set_state(DevState.OFF)

    @command()
    def turn_on(self):
        self.set_state(DevState.ON)


# start the server
if __name__ == "__main__":
    LockInAmp.run_server()

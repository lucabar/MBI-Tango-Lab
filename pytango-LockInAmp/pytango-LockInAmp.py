#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright (C) 2020  MBI-Division-B
# MIT License, refer to LICENSE file
# Author: Luca Barbera / Email: barbera@mbi-berlin.de


from tango import AttrWriteType, DevState, DebugIt, DispLevel
from tango.server import Device, attribute, command, device_property

import visa

class LockInAmp(Device):
    '''
    This docstring should describe your Tango Class and optionally
    what it depends on (drivers etc).
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

    # optionally use fget/fset to point to read and write functions.
    # Default is "read_temperature"/"write_temperature".
    # Added some optional attribute properties.
    phase = attribute(label='Phase',
                            dtype=float,
                            access=AttrWriteType.READ,
                            display_level=DispLevel.EXPERT,
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
        self.info_stream('Connection established')  # prints this line while -
        # in logging mode "info" or lower
        self.set_state(DevState.ON)

        rm = visa.ResourceManager('@py')
        self.inst = rm.open_resource('TCPIP::192.168.1.242')
        idn = self.inst.query('*IDN?')
        if idn:
            self.info_stream(idn)
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
    def dev_state(self):
        # possible pseudo code:
        # if hardware-state and TDS-state is ON:
        #   return DevState.ON
        # else:
        #   return DevState.FAULT
        return DevState

    def always_executed_hook(self):
        # a method that is executed continuously and by default does nothing.
        # if you want smth done polled/continuously, put it in this method.
        # check connection to hardware or whether status is acceptable etc.
        pass

# ------ Read/Write functions ------ #
    def read_X(self):  # this is default to read humidity
        self.inst.query
        return self.__X

    def read_Y(self):
        return self.__Y

    def read_R(self):
        return self.__R

    def read_phase(self):
        return self.__phase

# ------ Internal Methods ------ #
    # method that works with multiple input parameters only "inside" this code

    def internal_method(self, param1, param2):
        # do something with param1, param2
        pass


# ------ COMMANDS ------ #

    @DebugIt()  # let the execution of this command be logged in debugging mode
    @command()  # make method executable through the client -
    # (as opposed to just callable inside this code)
    def external_method(self, param):
        # this kind of method only allows one input parameter
        pass

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

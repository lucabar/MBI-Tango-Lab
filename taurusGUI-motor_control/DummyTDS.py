#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright (C) 2020  MBI-Division-B
# MIT License, refer to LICENSE file
# Author: Luca Barbera / Email: barbera@mbi-berlin.de

from tango import AttrWriteType, DevState, DebugIt
from tango.server import Device, attribute, command, device_property
from random import randint
import time
import numpy as np


class DummyTDS(Device):

    temperature = attribute(label='Temperature',
                            unit='K',
                            access=AttrWriteType.READ_WRITE,
                            dtype=float,
                            min_value=0)

    humidity = attribute(label='Humidity',
                         unit='%',
                         access=AttrWriteType.READ_WRITE,
                         dtype=float)

    shutter_open = attribute(label='Shutter open',
                             dtype=bool,
                             access=AttrWriteType.READ_WRITE)

    sine = attribute(label='Sine',
                     dtype=float,
                     access=AttrWriteType.READ_WRITE)

    pos = attribute(label='Position',
                    dtype=float,
                    access=AttrWriteType.READ_WRITE)

    dummynr = device_property(dtype=int)

    def init_device(self):
        self.info_stream('Connecting to dummy...')
        Device.init_device(self)
        self.set_state(DevState.ON)
        self.__temp = 300
        self.__humid = 42.5
        self.__shut = False
        self.__humidparam = 100
        self.__starttime = time.time()
        self.__freq = 1
        self.__pos = 0
        self.info_stream('Connection to dummy established.')

    def always_executed_hook(self):
        self.__humid = (randint(4200, 4700)+self.__humidparam)/100

    def read_pos(self):
        return self.__pos

    def write_pos(self, value):
        self.__pos = value

    def read_temperature(self):
        return self.__temp

    def write_temperature(self, value):
        if self.__shut:
            self.error_stream('Cannot write temperature when shutter is open')
            self.set_state(DevState.FAULT)
        else:
            self.__temp = value

    def write_humidity(self, value):
        self.__humidparam = value

    def read_humidity(self):
        return self.__humid

    def read_shutter_open(self):
        return self.__shut

    def write_shutter_open(self, value):
        self.__shut = value

    def read_sine(self):
        return 42*np.sin(self.__freq*(time.time()-self.__starttime))

    def write_sine(self, value):
        self.__freq = value

    @DebugIt()
    @command()
    def turn_on(self):
        self.set_state(DevState.ON)

    @DebugIt()
    @command()
    def turn_off(self):
        self.set_state(DevState.OFF)


if __name__ == "__main__":
    DummyTDS.run_server()

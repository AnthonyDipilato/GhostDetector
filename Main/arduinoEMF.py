
# interface for raspberry pi to communicate to the arduino via I2C

import smbus
import math
import time
import sys
import subprocess

class EMF:
    def __init__(self, port=1, address=0x04):
        self.bus = smbus.SMBus(port)
        self.address = address
        self.left = 0
        self.right = 0
        self.left_offset = -170
        self.right_offset = -130
    def update(self):
        try:
            self.bus.write_byte(self.address, 0)
            flag = 0
        except IOError:
            subprocess.call(['i2cdetect', '-y', '1'])
            flag = 1     #optional flag to signal your code to resend or something
        
        time.sleep(0.25) # give arduino a moment to respond
        data = self.bus.read_i2c_block_data(self.address, 1)
        self.left = data[0] + self.left_offset
        if self.left < 0:
            self.left = 0
        self.right = data[1] + self.right_offset
        if self.right < 0:
            self.right = 0
        return self.left,self.right



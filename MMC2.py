from re import L
import sys
import serial

try:
    import pyvisa
except:
    print("pyvisa is not available")
    sys.exit()

import numpy as np

class MMC2:
    def __init__(self, visaResourceManager:pyvisa.ResourceManager, dev) -> None:
        try :
            self.device_instance = visaResourceManager.open_resource(dev)
            self.rm = visaResourceManager
            print("Open device : " + dev)
        except:
            print("Cannot open device : " + dev)
        self.X = 0
        self.Y = 0
        
        self.__speed_limit = np.array([1000, 20000, 1000])
        self.__P2MM = 0.002

    def __del__(self):
        try:
            self.device_instance.close()
        except:
            print("Cannot close device.")

    def __mm2pulse(self, mm):
        return mm/self.__P2MM
    
    def __pulse2mm(self, p):
        return p*self.__P2MM
    
    def set_P2MM(self, P2MM):
        self.__P2MM = P2MM
    
    def set_speed_limit(self, sl = None):
        if(sl is None):
            self.set_speed_limit(self.__speed_limit)
        else:
            self.send("D:P" + str(sl[0]) + "P" + str(sl[1])+ "P" + str(sl[2]))
            self.__speed_limit = sl

    def move(self, x, y = 0):
        self.X = self.X + self.__mm2pulse(x)
        self.Y = self.Y + self.__mm2pulse(y)
        self.abs_move(self.X, self.Y)
    
    def abs_move(self, x, y):
        self.send("A:WP"+str(int(self.__mm2pulse(x)))+"P"+str(int(self.__mm2pulse(y))))
    
    def get_position(self):
        return self.__pulse2mm(self.X), self.__pulse2mm(self.Y)
    
    def get_position_pulses(self):
        return self.X, self.Y
    
    def go_mechanical_origin(self):
        self.X = 0.0
        self.Y = 0.0
        self.send("H:")
    
    def check_version(self) -> str:
        return self.query("?:")
    
    def wait(self):
        self.send("W:")
    
    def send(self, command:str):
        print((command+"\n"))
        self.device_instance.write((command+"\n"))
        
    def query(self, command:str) -> str:
        print((command+"\n"))
        self.device_instance.write((command+"\n"))
        
    def stop(self):
        self.send("L:W")
    
    def EMO(self):
        self.send("L:E")


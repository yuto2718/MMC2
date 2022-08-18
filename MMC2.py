import sys

try:
    import pyvisa
except:
    print("pyvisa is not available")
    sys.exit()

import numpy as np

class MMC2:
    def __init__(self, visaResourceManager:pyvisa.ResourceManager) -> None:
        self.rm = visaResourceManager
        self.device_instance = None
        
        self.X = 0
        self.Y = 0
        
        self.__speed_limit = np.array([0, 0])
        self.__P2MM = 0.002

    def __del__(self):
        try:
            self.inst.close()
        except:
            print("Cannot close device.")

    def __mm2pulse(self, mm):
        return mm/self.__P2MM
    
    def __pulse2mm(self, p):
        return p*self.__P2MM
    
    def set_P2MM(self, P2MM):
        self.__P2MM = P2MM
    
    def move(self, x, y = 0):
        self.X = self.X + self.__mm2pulse(x)
        self.Y = self.Y + self.__mm2pulse(y)
        self.abs_move(self.X, self.Y)
    
    def abs_move(self, x, y):
        self.send("A:WP"+str(x)+"P"+str(y))
    
    def get_position(self):
        return self.__pulse2mm(self.X), self.__pulse2mm(self.Y)
    
    def get_position_pulses(self):
        return self.X, self.Y
    
    def go_mechanical_origin(self):
        self.X = 0.0
        self.Y = 0.0
        self.send("H:")
        self.wait()
    
    def check_version(self) -> str:
        return self.query("?:")
    
    def wait(self):
        self.query("W:")
    
    def send(self, command:str):
        self.device_instance.write(command + "\r\n")
        print(command)
        
    def query(self, command:str) -> str:
        print(command)
        return self.device_instance.query(command + "\r\n")
    
    def stop(self):
        self.send("L:W")
    
    def EMO(self):
        self.send("L:E")
    
    def connect(self, name:str):
        try :
            self.device_instance = self.self.rm.open_resource(name)
            print("Open device : " + name)
        except:
            print("Cannot open device : " + name)
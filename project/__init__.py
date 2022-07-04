from . import module

class Project:
    def main(self):
        print(f'this is main {self}')
        sp = module.SerialPort()
        print(f'this is serialport {sp}')
        
        pass
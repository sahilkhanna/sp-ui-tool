from serial import Serial
from serial.tools import list_ports
class SerialPort:
    _selectedPortName:str
    def __init__(self, comPortName:str = None) -> None:
        availablePorts = self.list_serial_ports()
        if comPortName in availablePorts:
            self._selectedPortName = comPortName
        else:
            raise ValueError('Provided port doesn\'t exist')
        
    @staticmethod
    def list_serial_ports() -> dict:
        ports = list_ports.comports()
        portList = dict()
        for port, description, hwid in ports:
            portList.update({port : description})
        return portList
    

if __name__ == "__main__":
    
    ports = SerialPort.list_serial_ports()
    for comport in ports:
        sp = SerialPort(comport)
        print(sp._selectedPortName)
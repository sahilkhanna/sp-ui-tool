from serial import Serial
from serial.tools import list_ports
class SerialPort:
    _selectedPortName:str
    _conf={
        'baudrate':115200,
        'bytesize':8, 
        'parity':'N',
        'stopbits':1,
        'timeout':None,
        'xonxoff':0,
        'rtscts':0
    }
    def __init__(self, comPortName:str = None, conf:dict = None) -> None:
        availablePorts = self.list_serial_ports()
        if comPortName in availablePorts:
            self._selectedPortName = comPortName
        else:
            raise ValueError('Provided port doesn\'t exist')
        if conf:
            for setting in conf:
                if setting in self._conf:
                    self._conf[setting]=conf[setting]
                else:
                    raise ValueError(f'Unsupported or invalid setting {setting}')
        
        
    @staticmethod
    def list_serial_ports() -> dict:
        ports = list_ports.comports()
        portList = dict()
        for port, description, hwid in ports:
            portList.update({port : description})
        return portList
    

if __name__ == "__main__":
    
    ports = SerialPort.list_serial_ports()
    portSetting = {'baudrate':115200}
    for comport in ports:
        sp = SerialPort(comport,portSetting)
        print(sp._selectedPortName,sp._conf)
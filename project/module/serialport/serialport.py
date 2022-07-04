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
        'xonxoff':False,
        'rtscts':False
    }
    _sp:Serial
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
    
    def __enter__(self):
        self._sp = Serial()
        self._sp.port=self._selectedPortName
        self._sp.baudrate = self._conf['baudrate']
        self._sp.bytesize=self._conf['bytesize']
        self._sp.parity=self._conf['parity']
        self._sp.stopbits=self._conf['stopbits']
        self._sp.timeout=self._conf['timeout']
        self._sp.xonxoff=self._conf['xonxoff']
        self._sp.rtscts=self._conf['rtscts']
        self.connection = self._sp.open()
        return self.connection
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self._sp.close()
        print(f'Context ended for {self._selectedPortName}')
        
        
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
        try:
            with sp as serialport:
                print(serialport)
        except:
            pass
                
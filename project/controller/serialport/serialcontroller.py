from time import sleep
from tkinter import Frame
from serial import Serial
from serial.threaded import Protocol, ReaderThread
from serial.tools import list_ports
        
class FixedLengthPacketHandler(Protocol):
    """\
    Modified Protocol as used by the ReaderThread. 
    """
    PACKET_LENGTH = 256
    def __init__(self, controller):
        super().__init__()
        self.buffer = bytearray()
        self.controller = controller
        self.transport = None
        
    def connection_made(self, transport):
        """Called when reader thread is started"""
        super(FixedLengthPacketHandler, self).connection_made(transport)
        print(f'Serial connection made for {transport.serial.name}')
        self.transport = transport
        if self.controller and self.controller.connection_callback:
            self.controller.connection_callback()

    def data_received(self, data):
        """\
        Called when data is received from the serial port
        Append bytes till buffer is full and handle the packet.
        """
        self.buffer.extend(data)
        if len(self.buffer) >= self.PACKET_LENGTH:
            temp_buff = self.buffer[:self.PACKET_LENGTH]
            self.buffer = self.buffer[self.PACKET_LENGTH:]
            print(f'data:{temp_buff}')
            # TODO: Handle this
            
    
    def send_data(self, data):
        """\
        Called when serialport needs to send data. You may format it 
        accordingly
        """
        self.transport.write(data)

    def connection_lost(self, exc):
        """\
        Called when the serial port is closed or the reader loop terminated
        otherwise.
        """
        print(f'Connection Lost')
        self.transport = None
        if self.controller and self.controller.disconnection_callback:
            self.controller.disconnection_callback()
        if isinstance(exc, Exception):
            raise exc
        
class SerialController:
    _selectedPortName:str
    _conf={
        'baudrate':115200,
        'bytesize':8, 
        'parity':'N',
        'stopbits':1,
        'timeout':1,
        'xonxoff':False,
        'rtscts':False
    }
    _sp:Serial
    _rt:ReaderThread
    _proto:FixedLengthPacketHandler
    
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
        
        self.connection_callback = lambda : print('connection_callback')
        self.disconnection_callback = lambda : print('disconnection_callback')
        self._sp = Serial(self._selectedPortName)
        self._sp.baudrate = self._conf['baudrate']
        self._sp.bytesize=self._conf['bytesize']
        self._sp.parity=self._conf['parity']
        self._sp.stopbits=self._conf['stopbits']
        self._sp.timeout=self._conf['timeout']
        self._sp.xonxoff=self._conf['xonxoff']
        self._sp.rtscts=self._conf['rtscts']
        
    def connect(self):
        '''\
        Attempts to connect to the specified serial port
        '''
        self._rt = ReaderThread(self._sp, self.serial_packet_handler)
        self._rt.start()
                
    def disconnect(self):
        '''\
        Attempts to disconnect to the specified serial port
        '''
        if self._rt is not None:
            try:
                self._rt.close()
            except Exception as e:
                print(f'Exception {e} during serial disconnect')
        self._rt = None
    
    def __enter__(self):
        self.connect()
        return self._proto
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.disconnect()
        self._sp = None
        print(f'Context ended for {self._selectedPortName}')
        print(exc_type)
    
    def serial_packet_handler(self):
        self._proto = FixedLengthPacketHandler(self)
        return self._proto
        
    @staticmethod
    def list_serial_ports() -> dict:
        ports = list_ports.comports()
        portList = dict()
        for port, description, hwid in ports:
            portList.update({port : description})
        return portList

    

if __name__ == "__main__":
    TEST_PORT = 'COM8'
    ports = SerialController.list_serial_ports()
    portSetting = {'baudrate':115200}
    sPort = SerialController(TEST_PORT, portSetting)
    with sPort as device:
        sleep(1)
    print('End')
    
                
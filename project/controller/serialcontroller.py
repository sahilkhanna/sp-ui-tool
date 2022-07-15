from time import sleep
from serial import Serial, SerialException
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
        self.buffer = bytearray()
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
            # TODO: Handle this
            if self.controller and self.controller.handle_packet:
                convhex = " ".join(["{:02x}".format(bytes) for bytes in temp_buff])
                self.controller.handle_packet('[RX]: ' + convhex.upper())
            
    
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
        self.buffer = bytearray()
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
        
        self._sp = None
        if conf:
            for setting in conf:
                if setting in self._conf:
                    self._conf[setting]=conf[setting]
                else:
                    raise ValueError(f'Unsupported or invalid setting {setting}')
        
        if comPortName:
            self.set_comport(comPortName)
            
        self.connection_callback = lambda : print('connection_callback')
        self.disconnection_callback = lambda : print('disconnection_callback')
        self.handle_packet = lambda : print('handle_packet')
    
    def set_comport(self, comPortName):
        '''\
        Set comport
        '''
        availablePorts = self.list_serial_ports()
        if comPortName in availablePorts:
            if self._sp:
                self.disconnect()
                self._sp = None
            self._selectedPortName = comPortName
            try:
                self._sp = Serial(self._selectedPortName)
                self._sp.baudrate = self._conf['baudrate']
                self._sp.bytesize=self._conf['bytesize']
                self._sp.parity=self._conf['parity']
                self._sp.stopbits=self._conf['stopbits']
                self._sp.timeout=self._conf['timeout']
                self._sp.xonxoff=self._conf['xonxoff']
                self._sp.rtscts=self._conf['rtscts']
                self._rt = ReaderThread(self._sp, self.serial_packet_handler)
            except SerialException as e:
                print(f'Cannot open COM Port:{self._selectedPortName}, {e}')
        else:
            raise ValueError('Port {comPortName} doesn\'t exist')
        
    def connect(self):
        '''\
        Attempts to connect to the specified serial port
        '''
        try:
            self._rt.start()
        except AttributeError as e:
            print(f'Cannot connect to port:{self._selectedPortName}, {e}')
                
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
    
    def send_packet(self, msg):
        self._proto.send_data(msg)
    
    def serial_packet_handler(self):
        self._proto = FixedLengthPacketHandler(self)
        return self._proto
        
    @staticmethod
    def list_serial_ports() -> list:
        ports = list_ports.comports()
        portList = list()
        for port, description, hwid in ports:
            portList.append(port)
        return portList

    

if __name__ == "__main__":
    TEST_PORT = 'COM9'
    ports = SerialController.list_serial_ports()
    portSetting = {'baudrate':115200}
    sPort = SerialController(TEST_PORT, portSetting)
    with sPort as device:
        sleep(1)
    print('End')
    
                
from enum import Enum
from time import sleep
from serial import Serial, SerialException
from serial.threaded import Protocol, ReaderThread, LineReader
from serial.tools import list_ports


class PacketHandlers(Enum):
    FIXED_PACKET = 0
    LINE_READER = 1
    
    
if __name__ == "__main__":
    a = [handler.name for handler in PacketHandlers]
    b = PacketHandlers[a[0]]
    print(b)

from project.model.main import MainModel

class FixedLengthPacketHandler(Protocol):
    """\
    Modified Protocol as used by the ReaderThread.
    """
    PACKET_LENGTH = 256
    isConnected: bool

    def __init__(self, controller):
        super().__init__()
        self.buffer = bytearray()
        self.controller = controller
        self.transport = None
        self.isConnected = False

    def clear_buffer(self):
        self.buffer = bytearray()

    def connection_made(self, transport):
        """Called when reader thread is started"""
        super(FixedLengthPacketHandler, self).connection_made(transport)
        self.transport = transport
        self.clear_buffer()
        self.isConnected = True
        if self.controller and self.controller.connection_callback:
            self.controller.connection_callback()

    def chunk_and_handle_packets(self, big_buff: bytearray) -> bytearray:
        small_buff = big_buff[:self.PACKET_LENGTH]
        big_buff = big_buff[self.PACKET_LENGTH:]
        if self.controller and self.controller.handle_packet:
            convhex = " ".join(["{:02x}".format(bytes) for bytes in small_buff])
            self.controller.handle_packet(f'{convhex.upper()}')
        while len(big_buff) >= len(small_buff):
            small_buff = big_buff[:self.PACKET_LENGTH]
            big_buff = big_buff[self.PACKET_LENGTH:]
            if self.controller and self.controller.handle_packet:
                convhex = " ".join(["{:02x}".format(bytes) for bytes in small_buff])
                self.controller.handle_packet(f'{convhex.upper()}')
        return big_buff

    def data_received(self, data):
        """\
        Called when data is received from the serial port
        Append bytes till buffer is full and handle the packet.
        """
        self.buffer.extend(data)
        if len(self.buffer) >= self.PACKET_LENGTH:
            self.buffer = self.chunk_and_handle_packets(self.buffer)

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
        self.transport = None
        self.clear_buffer()
        self.isConnected = False
        if self.controller and self.controller.disconnection_callback:
            self.controller.disconnection_callback()
        if isinstance(exc, Exception):
            raise exc


class SerialController:
    _selectedPortName: str
    _conf = {
        'baudrate': 115200,
        'bytesize': 8,
        'parity': 'N',
        'stopbits': 1,
        'timeout': 1,
        'xonxoff': False,
        'rtscts': False
    }
    _sp: Serial
    _rt: ReaderThread
    packetHandlers = {
        PacketHandlers.FIXED_PACKET: FixedLengthPacketHandler,
        PacketHandlers.LINE_READER: LineReader
    }

    def __init__(self, model: MainModel) -> None:

        self._sp = None
        self._proto = None
        self._model = model
        conf = self._model.get_all_port_settings()
        if conf:
            for setting in conf:
                if setting in self._conf:
                    self._conf[setting] = conf[setting]
                else:
                    raise ValueError(f'Unsupported or \
                        invalid setting {setting}')
        self.connection_callback = lambda: print('connection_callback')
        self.disconnection_callback = lambda: print('disconnection_callback')
        self.handle_packet = lambda: print('handle_packet')

    def set_comport(self, comPortName: str, conf: dict = None):
        '''\
        Set comport
        '''
        availablePorts = self.list_serial_ports()
        if comPortName in availablePorts:
            if self._sp:
                if self._sp.is_open:
                    self.disconnect()
                self._sp = None
            self._selectedPortName = comPortName
            try:
                if conf:
                    self._conf = conf
                self._sp = Serial(self._selectedPortName)
                self._sp.baudrate = self._conf['baudrate']
                self._sp.bytesize = self._conf['bytesize']
                self._sp.parity = self._conf['parity']
                self._sp.stopbits = self._conf['stopbits']
                self._sp.timeout = self._conf['timeout']
                self._sp.xonxoff = self._conf['xonxoff']
                self._sp.rtscts = self._conf['rtscts']
                self._rt = ReaderThread(self._sp, self.serial_packet_handler)
            except SerialException as e:
                print(f'Cannot open COM Port:{self._selectedPortName}, {e}')
        else:
            raise ValueError(f'Port {comPortName} doesn\'t exist')

    def connect(self):
        '''\
        Attempts to connect to the specified serial port
        '''
        try:
            self.clear_rx_buffer()
            self._rt.start()
        except AttributeError as e:
            print(f'Cannot connect to port:{self._selectedPortName}, {e}')

    def disconnect(self):
        '''\
        Attempts to disconnect to the specified serial port
        '''
        if self._proto is not None:
            self.clear_rx_buffer()
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

    def set_packet_handler(self, handler: PacketHandlers):
        self._proto = self.packetHandlers[handler](self)
        self._rt = ReaderThread(self._sp, self._proto)

    def serial_packet_handler(self):
        self._proto = self.packetHandlers["fixed_length"](self)
        return self._proto

    def clear_rx_buffer(self):
        if self._proto is not None:
            self._proto.clear_buffer()

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
    portSetting = {'baudrate': 115200}
    sPort = SerialController()
    sPort.set_comport(TEST_PORT)
    with sPort as device:
        sleep(1)
    print('End')

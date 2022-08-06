
from project.controller.serialcontroller import SerialController
from project.controller.serialcontroller import PacketHandlers
from project.model.main import MainModel


class MainController():

    def __init__(self, model: MainModel) -> None:
        self._mainModel = model
        self._serialController = SerialController(self._mainModel)
        pass

    def set_device_port(self, comPort: str):
        self._serialController.set_comport(
            comPortName=comPort,
            conf=self._mainModel.get_all_port_settings())
        self._mainModel.update_port_name(comPort)

    def connect_to_device(self):
        self._serialController.connect()

    def disconnect_from_device(self):
        self._serialController.disconnect()

    def send_packet(self, msg):
        self._serialController.send_packet(msg)

    def update_port_baudrate(self, baudrate):
        self._mainModel.update_setting_baudrate(baudrate)
        self._serialController.set_comport(
            comPortName=self._mainModel.get_port_name(),
            conf=self._mainModel.get_all_port_settings())

    def update_packet_handler(self, handler: PacketHandlers):
        self._serialController.set_packet_handler(handler)

    def update_serial_cb(self, handlePacketCb, connectionCb, disconnectionCb):
        self._serialController.handle_packet = handlePacketCb
        self._serialController.connection_callback = connectionCb
        self._serialController.disconnection_callback = disconnectionCb

    def clear_serial_rx_buffer(self) -> None:
        self._serialController.clear_rx_buffer()

    def save_project_settings(self, filename: str):
        self._mainModel.save_project_file(filename)

    def open_project_settings(self, filename: str):
        self._mainModel.load_project_file(filename)

    def update_send_sequence(self, sequence: list):
        self._mainModel.update_send_sequence(sequence)

    def get_send_sequences(self) -> list:
        return self._mainModel.get_sequences()

    def get_saved_port_name(self) -> str:
        return self._mainModel.get_port_name()

    def list_serial_ports(self) -> list:
        return self._serialController.list_serial_ports()

import json
from project.util import return_as_int


class MainModel():
    def __init__(self) -> None:
        self._portName = ''
        self._portSettings = {
            'baudrate': 115200,
            'bytesize': 8,
            'parity': 'N',
            'stopbits': 1,
            'timeout': 1,
            'xonxoff': False,
            'rtscts': False
            }
        self._sendSequence = []

    def get_all_port_settings(self) -> dict:
        return self._portSettings

    def update_port_name(self, portName: str):
        self._portName = portName

    def get_port_name(self) -> str:
        return self._portName

    def update_setting_baudrate(self, baudrate: int):
        self._portSettings['baudrate'] = return_as_int(baudrate)

    def update_setting_bytesize(self, bytesize: int):
        self._portSettings['bytesize'] = return_as_int(bytesize)

    def update_setting_parity(self, parity):
        self._portSettings['parity'] = parity

    def update_setting_stopbits(self, stopbits: int):
        self._portSettings['stopbits'] = return_as_int(stopbits)

    def update_setting_timeout(self, timeout: int):
        self._portSettings['timeout'] = return_as_int(timeout)

    def update_setting_xonxoff(self, xonxoff: bool):
        self._portSettings['xonxoff'] = xonxoff

    def update_setting_rtscts(self, rtscts: bool):
        self._portSettings['rtscts'] = rtscts

    def update_send_sequence(self, sequence: list) -> None:
        self._sendSequence = sequence

    def get_sequences(self) -> list:
        return self._sendSequence

    def update_packet_handler(self, packethandler: str) -> None:
        self._packetHandler = packethandler

    def get_packet_handler(self) -> str:
        return self._packetHandler

    def save_project_file(self, filepath: str):
        outData = {
            'port': self._portName,
            'portSetting': self._portSettings,
            'sequences': self._sendSequence,
            'packetHandler': self._packetHandler
        }
        with open(filepath, "w+") as outfile:
            json.dump(outData, outfile)

    def load_project_file(self, filepath: str) -> bool:
        projectSetting = {}
        with open(filepath, 'r') as projectFile:
            projectSetting = json.load(projectFile)
            if 'sequences' in projectSetting:
                self._sendSequence = projectSetting['sequences']
            if 'port' in projectSetting:
                self._portName = projectSetting['port']
            if 'portSetting' in projectSetting:
                self._portSettings = projectSetting['portSetting']
            if 'packetHandler' in projectSetting:
                self._packetHandler = projectSetting['packetHandler']
        return True

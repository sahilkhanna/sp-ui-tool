import json
class MainModel():
    def __init__(self) -> None:
        self._portSettings = {
        'baudrate':115200,
        'bytesize':8,
        'parity':'N',
        'stopbits':1,
        'timeout':1,
        'xonxoff':False,
        'rtscts':False
        }
        self._sendSequence=[]
    
    def get_all_port_settings(self)->dict:
        return self._portSettings
    
    # def update_setting_serialPortName(self, portName):
    #     self._portSettings['serialPortName'] = portName   
    def update_setting_baudrate(self, baudrate:int):
        self._portSettings['baudrate'] = baudrate           
    def update_setting_bytesize(self, bytesize:int):
        self._portSettings['bytesize'] = bytesize
    def update_setting_parity(self, parity):
        self._portSettings['parity'] = parity
    def update_setting_stopbits(self, stopbits:int):
        self._portSettings['stopbits'] = stopbits
    def update_setting_timeout(self, timeout:int):
        self._portSettings['timeout'] = timeout
    def update_setting_xonxoff(self, xonxoff:bool):
        self._portSettings['xonxoff'] = xonxoff
    def update_setting_rtscts(self, rtscts:bool):
        self._portSettings['rtscts'] = rtscts
        
    def update_send_sequence(self, sequence:list)->None:
        self._sendSequence = sequence
    def get_sequences(self)->list:
        return self._sendSequence
    
    def save_project_file(self, filepath:str):
        outData = {
            'portSetting':self._portSettings,
            'sequences':self._sendSequence
        }
        with open(filepath, "w+") as outfile:
            json.dump(outData, outfile)
    
    def load_project_file(self, filepath:str)->bool:
        projectSetting={}
        with open(filepath, 'r') as projectFile:
            projectSetting = json.load(projectFile)
            if 'sequences' in  projectSetting:
                self._sendSequence = projectSetting['sequences']
        return True
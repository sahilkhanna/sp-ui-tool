from faulthandler import disable
from operator import contains
import PySimpleGUI as gui
from project.controller.serialcontroller import SerialController
class MainUI:
    KEY_MSG_LIST = "MSG_LIST"
    KEY_PORT_LIST = "PORT_LIST"
    KEY_ADD_MSG_BTN = "ADD_MSG_BTN"
    KEY_REMOVE_MSG_BTN = "REMOVE_MSG_BTN"
    KEY_SEND_MSG_BTN = "SEND_MSG_BTN"
    KEY_REFRESH_PORT_LIST = "REFRESH_PORT_LIST"
    KEY_OPEN_PORT = "OPEN_PORT"
    KEY_SEND_MSG_INPUT = "SEND_MSG_INPUT"
    
    KEY_CONSOLE = "CONSOLE"
    KEY_CLEAR_TERMINAL = "CLEAR_TERMINAL_BTN"
    KEY_CONSOLE_MENU_COPY_SELECTED = "Copy Selected"
    KEY_CONSOLE_MENU_COPY_ALL = "Copy All"
    CONSOLE_RIGHT_CLICK_MENU = ['',[KEY_CONSOLE_MENU_COPY_SELECTED, KEY_CONSOLE_MENU_COPY_ALL]]
    
    APPEND_TX_MSG = "[TX]: "
    
    LEFT_COLUMN_WIDTH = 40
    RIGHT_COLUMN_WIDTH = 80
    _controller: SerialController
    def __init__(self, title:str, controller) -> None:
        self._controller = controller
        self._msgList = []
        # First the window layout in 2 columns
        gui.theme('DarkBlue')
        conf_column = [
            [gui.Text("Config:")],
                [gui.Combo(values="",tooltip="Select Com Port", readonly=True, default_value="Select Port", 
                           size=self.LEFT_COLUMN_WIDTH-20, enable_events=True, key=self.KEY_PORT_LIST),
                 gui.Push(), gui.Button(button_text='Refresh', key=self.KEY_REFRESH_PORT_LIST),
                 gui.Button(button_text='Open', key=self.KEY_OPEN_PORT)],
                [gui.HSeparator()],
            [gui.Input(default_text='', background_color='#0a1016', disabled_readonly_background_color='#16232e', 
                       size=(self.LEFT_COLUMN_WIDTH-5, 20), key=self.KEY_SEND_MSG_INPUT),
             gui.Button(button_text='Send', key=self.KEY_SEND_MSG_BTN, disabled=True)],
            [gui.Listbox(values=self._msgList, select_mode=gui.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, 
                         size=(self.LEFT_COLUMN_WIDTH, 20), background_color='#0a1016', key=self.KEY_MSG_LIST)],
            [gui.Push(), gui.Button(button_text='+', key=self.KEY_ADD_MSG_BTN, size=(5,1)),
             gui.Button(button_text='-', key=self.KEY_REMOVE_MSG_BTN, size=(5,1)),]
        ]
        # For now will only show the name of the file that was chosen
        console_column = [
            [gui.Text("Console:"), gui.Push(),
             gui.Button(button_text='Clear', key=self.KEY_CLEAR_TERMINAL)],
            [gui.Multiline(size=(self.RIGHT_COLUMN_WIDTH, 26), write_only=True, 
                           background_color='#0a1016', text_color='green', key=self.KEY_CONSOLE)],
        ]
        # ----- Full layout -----
        self._layout = [
            [gui.Column(conf_column),
            gui.VSeperator(),
            gui.Column(console_column),]
        ]
        self._ui = gui.Window(title, self._layout)
        gui.cprint_set_output_destination(self._ui, self.KEY_CONSOLE)
        self._isConnected = False

    def refresh_port_list(self):
        portList=self._controller.list_serial_ports()
        self._ui[self.KEY_PORT_LIST].update(values=portList, set_to_index=0)
        if len(portList) != 0:
            self._controller.set_comport(self._ui[self.KEY_PORT_LIST].get())
        
    def open_port_connection(self):
        self._controller.connect()
        self._ui[self.KEY_PORT_LIST].update(disabled=True)
        self._ui[self.KEY_OPEN_PORT].update(text='Close')
        self._ui[self.KEY_SEND_MSG_BTN].update(disabled=False)
        self._isConnected = True
        
    def close_port_connection(self):
        self._controller.disconnect()
        self._ui[self.KEY_PORT_LIST].update(disabled=False)
        self._ui[self.KEY_OPEN_PORT].update(text='Open')
        self._ui[self.KEY_SEND_MSG_BTN].update(disabled=True)
        self._isConnected = False
        self.refresh_port_list()
        
    def update_msg_list(self, msg, append:bool):
        if append:
            if msg:
                self._msgList.append(msg)
        else:
            if msg in self._msgList:
                self._msgList.remove(msg)
        self._ui[self.KEY_MSG_LIST].update(values=self._msgList)
        
    def update_send_msg_input(self, msg):
        if msg is not None:
            self._ui[self.KEY_SEND_MSG_INPUT].update(value=msg)
        
    def send_msg(self, msg:str):
        if len(msg) > 0:
            self._controller.send_packet(msg.encode())
            self.update_console(self.APPEND_TX_MSG + msg)
        
    def update_console(self, msg):
        if self.APPEND_TX_MSG in msg:
            gui.cprint(msg, t='green')
        else:
            gui.cprint(msg, t='red')
        
    def launch(self):
        self._controller.handle_packet=self.update_console
        event, values = self._ui.read(timeout=10)
        self.refresh_port_list()
        while True:
            event, values = self._ui.read(timeout=10)
            if event == gui.WIN_CLOSED:
                break
            elif event == self.KEY_REFRESH_PORT_LIST:
                self.refresh_port_list()
            elif event == self.KEY_PORT_LIST:
                self._controller.set_comport(values[self.KEY_PORT_LIST])
            elif event == self.KEY_OPEN_PORT:
                if self._isConnected:
                    self.close_port_connection()
                else:
                    self.open_port_connection()
            elif event == self.KEY_CLEAR_TERMINAL:
                self._ui[self.KEY_CONSOLE].update(value='')
            elif event == self.KEY_ADD_MSG_BTN:
                self.update_msg_list(values[self.KEY_SEND_MSG_INPUT], True)
            elif event == self.KEY_REMOVE_MSG_BTN:
                self.update_msg_list(values[self.KEY_SEND_MSG_INPUT], False)
            elif event == self.KEY_SEND_MSG_BTN:
                self.send_msg(values[self.KEY_SEND_MSG_INPUT])
            elif event == self.KEY_MSG_LIST:
                self.update_send_msg_input(values[self.KEY_MSG_LIST][0])
            
                

        # Finish up by removing from the screen
        self._ui.close()
from faulthandler import disable
import PySimpleGUI as gui
from project.controller.serialcontroller import SerialController
class MainUI:
    KEY_CONSOLE = "CONSOLE"
    KEY_MSG_LIST = "MSG_LIST"
    KEY_PORT_LIST = "PORT_LIST"
    KEY_ADD_MSG_BTN = "ADD_MSG_BTN"
    KEY_SEND_MSG_BTN = "SEND_MSG_BTN"
    KEY_REFRESH_PORT_LIST = "REFRESH_PORT_LIST"
    KEY_OPEN_PORT = "OPEN_PORT"
    KEY_CLEAR_TERMINAL = "CLEAR_TERMINAL_BTN"
    LEFT_COLUMN_WIDTH = 40
    RIGHT_COLUMN_WIDTH = 80
    _controller: SerialController
    def __init__(self, title:str, controller) -> None:
        self._controller = controller
        # First the window layout in 2 columns
        gui.theme('DarkBlue')
        conf_column = [
            [gui.Text("Config:")],
                [gui.Combo(values="",tooltip="Select Com Port", readonly=True, default_value="Select Port", size=self.LEFT_COLUMN_WIDTH-20, enable_events=True, key=self.KEY_PORT_LIST),
                 gui.Button(button_text='Refresh', key=self.KEY_REFRESH_PORT_LIST),
                 gui.Button(button_text='Open', key=self.KEY_OPEN_PORT)],
                [gui.HSeparator()],
            [gui.Button(button_text='Add Message', key=self.KEY_ADD_MSG_BTN),
             gui.Button(button_text='Send', key=self.KEY_SEND_MSG_BTN)],
            [gui.Listbox(values=[], select_mode=gui.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size=(self.LEFT_COLUMN_WIDTH, 20), background_color='#0a1016', key=self.KEY_MSG_LIST)],
        ]
        # For now will only show the name of the file that was chosen
        console_column = [
            [gui.Text("Console:"),
             gui.Button(button_text='Clear', key=self.KEY_CLEAR_TERMINAL)],
            [gui.Multiline(size=(self.RIGHT_COLUMN_WIDTH, 22), write_only=True,background_color='#0a1016', text_color='green', key=self.KEY_CONSOLE)],
        ]
        # ----- Full layout -----
        self._layout = [
            [gui.Column(conf_column),
            gui.VSeperator(),
            gui.Column(console_column),]
        ]
        self._ui = gui.Window(title, self._layout)
        self._isConnected = False

    def refresh_port_list(self):
        self._ui[self.KEY_PORT_LIST].update(values=self._controller.list_serial_ports(), set_to_index=0)
        self._controller.set_comport(self._ui[self.KEY_PORT_LIST].get())
        
    def open_port_connection(self):
        self._controller.connect()
        self._ui[self.KEY_PORT_LIST].update(disabled=True)
        self._ui[self.KEY_OPEN_PORT].update(text='Close')
        self._isConnected = True
        
    def close_port_connection(self):
        self._controller.disconnect()
        self._ui[self.KEY_PORT_LIST].update(disabled=False)
        self._ui[self.KEY_OPEN_PORT].update(text='Open')
        self._isConnected = False
        self.refresh_port_list()
        
    def update_console(self, msg:bytearray):
        self._consoleBuffer = msg.decode("utf-8")
        self._ui[self.KEY_CONSOLE].print(msg)
        
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
                pass
                

        # Finish up by removing from the screen
        self._ui.close()
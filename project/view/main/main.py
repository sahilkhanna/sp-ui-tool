from faulthandler import disable
import PySimpleGUI as gui
from project.controller.serialport.serialcontroller import SerialController
class MainUI:
    KEY_CONSOLE = "CONSOLE"
    KEY_MSG_LIST = "MSG_LIST"
    KEY_PORT_LIST = "PORT_LIST"
    KEY_ADD_MSG_BTN = "ADD_MSG_BTN"
    KEY_SEND_MSG_BTN = "SEND_MSG_BTN"
    KEY_REFRESH_PORT_LIST = "REFRESH_PORT_LIST"
    KEY_OPEN_PORT = "OPEN_PORT"
    LEFT_COLUMN_WIDTH = 40
    RIGHT_COLUMN_WIDTH = 80
    _controller: SerialController
    def __init__(self, title:str, controller) -> None:
        self._controller = controller
        # First the window layout in 2 columns
        gui.theme('DarkBlue')
        conf_column = [
            [gui.Text("Console:")],
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
            [gui.Text("Console:")],
            [gui.Output(size=(self.RIGHT_COLUMN_WIDTH, 22), background_color='#0a1016', text_color='green', key=self.KEY_CONSOLE)],
        ]
        # ----- Full layout -----
        self._layout = [
            [gui.Column(conf_column),
            gui.VSeperator(),
            gui.Column(console_column),]
        ]
        self._ui = gui.Window(title, self._layout)
    pass

    def launch(self):
        console_text=""
        while True:
            event, values = self._ui.read()
            print(f'event = {event}, values = {values}')
            if event == gui.WIN_CLOSED:
                break
            elif event == self.KEY_REFRESH_PORT_LIST:
                self._ui[self.KEY_PORT_LIST].update(values=self._controller.list_serial_ports(), set_to_index=0)
            console_text += "hey\n"
            # self._ui[self.KEY_CONSOLE].update(value=console_text)
            # End program if user closes window or
            # presses the OK button

        # Finish up by removing from the screen
        self._ui.close()
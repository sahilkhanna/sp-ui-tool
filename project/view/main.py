from datetime import datetime
import PySimpleGUI as gui
from project.controller.maincontroller import MainController

ICON_FILE_PATH = 'assets/logo.ico'


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
    CONSOLE_RIGHT_CLICK_MENU = ['',
                                [KEY_CONSOLE_MENU_COPY_SELECTED,
                                 KEY_CONSOLE_MENU_COPY_ALL]]
    EV_MENU_OPEN_PROJECT = 'Open Project'
    EV_MENU_SAVE_PROJECT = 'Save'
    EV_MENU_SAVE_AS_PROJECT = 'Save as'
    EV_MENU_QUIT = 'Quit'
    EV_MENU_ABOUT = '&About'
    EV_MENU_BAUDRATE_9600 = '9600'
    EV_MENU_BAUDRATE_19200 = '19200'
    EV_MENU_BAUDRATE_38400 = '38400'
    EV_MENU_BAUDRATE_57600 = '57600'
    EV_MENU_BAUDRATE_115200 = '115200'
    BAUD_RATES = [EV_MENU_BAUDRATE_9600,
                  EV_MENU_BAUDRATE_19200,
                  EV_MENU_BAUDRATE_38400,
                  EV_MENU_BAUDRATE_57600,
                  EV_MENU_BAUDRATE_115200]
    MENU_DEF = [['&File',
                 [EV_MENU_OPEN_PROJECT,
                  EV_MENU_SAVE_PROJECT,
                  EV_MENU_SAVE_AS_PROJECT,
                  EV_MENU_QUIT]],
                ['&Settings',
                 ['&Baudrate',
                  BAUD_RATES,
                  '&Encoding',
                  ['bytes', 'string']]
                 ],
                ['&Help', EV_MENU_ABOUT]]
    APPEND_TX_MSG = "[TX -"
    APPEND_RX_MSG = "[RX -"
    LEFT_COLUMN_WIDTH = 40
    RIGHT_COLUMN_WIDTH = 80
    _controller: MainController

    def __init__(self, title: str, controller: MainController) -> None:
        self._controller = controller
        self._msgList = []
        # First the window layout in 2 columns
        gui.theme('DarkBlue')
        conf_column = [[gui.Text("Project Setting:")],
                       [gui.Combo(values="",
                        tooltip="Select Com Port",
                        readonly=True,
                        default_value="Select Port",
                        size=self.LEFT_COLUMN_WIDTH-20,
                        enable_events=True,
                        key=self.KEY_PORT_LIST),
                        gui.Push(),
                        gui.Button(button_text='Refresh',
                                   key=self.KEY_REFRESH_PORT_LIST),
                        gui.Button(button_text='Open',
                                   key=self.KEY_OPEN_PORT,
                                   size=(8, 1))],
                       [gui.HSeparator()],
                       [gui.Input(default_text='',
                                  background_color='#0a1016',
                                  disabled_readonly_background_color='#16232e',
                                  size=(self.LEFT_COLUMN_WIDTH-5, 20),
                                  key=self.KEY_SEND_MSG_INPUT),
                        gui.Button(button_text='Send',
                                   key=self.KEY_SEND_MSG_BTN,
                                   disabled=True)],
                       [gui.Listbox(values=self._msgList,
                                    select_mode=gui.LISTBOX_SELECT_MODE_SINGLE,
                                    enable_events=True,
                                    size=(self.LEFT_COLUMN_WIDTH, 20),
                                    background_color='#0a1016',
                                    key=self.KEY_MSG_LIST,
                                    horizontal_scroll=True,
                                    expand_x=True,
                                    expand_y=True)],
                       [gui.Push(),
                        gui.Button(button_text='+',
                                   key=self.KEY_ADD_MSG_BTN,
                                   tooltip='Add Message to list',
                                   size=(5, 1)),
                        gui.Button(button_text='-',
                                   key=self.KEY_REMOVE_MSG_BTN,
                                   tooltip='Remove Message to list',
                                   size=(5, 1))
                        ]
                       ]
        console_column = [
            [gui.Text("Console:"), gui.Push(),
             gui.Button(button_text='Clear', key=self.KEY_CLEAR_TERMINAL)],
            [gui.Multiline(size=(self.RIGHT_COLUMN_WIDTH, 26), write_only=True,
                           background_color='#0a1016',
                           text_color='green',
                           key=self.KEY_CONSOLE,
                           expand_x=True, expand_y=True)],
        ]
        # ----- Full layout -----
        self._layout = [
            [gui.Menu(self.MENU_DEF, key='menu')],
            [gui.Column(conf_column, expand_x=True, expand_y=True),
             gui.VSeperator(),
             gui.Column(console_column, expand_x=True, expand_y=True),
             ]
        ]
        self._ui = gui.Window(title, self._layout, resizable=True,
                              icon=ICON_FILE_PATH)
        gui.cprint_set_output_destination(self._ui, self.KEY_CONSOLE)
        self._isConnected = False

    def set_port(self, portName: str):
        self._controller.set_device_port(portName)
        self._ui[self.KEY_PORT_LIST].update(value=portName)

    def refresh_port_list(self):
        portList = self._controller.list_serial_ports()
        self._ui[self.KEY_PORT_LIST].update(values=portList, set_to_index=0)
        if len(portList) != 0:
            self.set_port(self._ui[self.KEY_PORT_LIST].get())

    def open_port_connection(self):
        self._ui[self.KEY_PORT_LIST].update(disabled=True)
        self._ui[self.KEY_OPEN_PORT].update(text='Opening')
        self._ui.read(timeout=1)
        self._controller.connect_to_device()

    def port_connected_cb(self):
        self._ui[self.KEY_SEND_MSG_BTN].update(disabled=False)
        self._isConnected = True
        self.enable_menu_item('&Settings')

    def close_port_connection(self):
        self._ui[self.KEY_OPEN_PORT].update(text='Closing')
        self._ui.read(timeout=1)
        self._controller.disconnect_from_device()

    def port_disconnected_cb(self):
        self._isConnected = False
        self.refresh_port_list()
        self.enable_menu_item('!&Settings', False)

    def update_msg_list(self, msg, append: bool):
        if append:
            if msg:
                self._msgList.append(msg)
        else:
            if msg in self._msgList:
                self._msgList.remove(msg)
        self._ui[self.KEY_MSG_LIST].update(values=self._msgList)
        self._controller.update_send_sequence(self._msgList)

    def update_send_msg_input(self, msg):
        if msg is not None:
            self._ui[self.KEY_SEND_MSG_INPUT].update(value=msg)

    def send_msg(self, msg: str):
        if len(msg) > 0:
            self._controller.send_packet(bytearray.fromhex(msg))
            self.update_console(msg, True)
        else:
            gui.popup_error("Message is empty! No can do",
                            title="Yuck",
                            auto_close=True,
                            auto_close_duration=3,
                            no_titlebar=True,
                            icon=ICON_FILE_PATH)

    def update_console(self, msg, isTX=False):
        if isTX:
            gui.cprint(f'{self.APPEND_TX_MSG} {datetime.now()}]: {msg}', t='green') # NOQA
        else:
            gui.cprint(f'{self.APPEND_RX_MSG} {datetime.now()}]: {msg}', t='red') # NOQA

    def about_popup(self):
        gui.popup('Serial Port Gui Tool',
                  'Sahil Khanna',
                  'https://github.com/sahilkhanna/sp-ui-tool',
                  grab_anywhere=True,
                  icon=ICON_FILE_PATH)

    def popup_error(self, msg: str):
        gui.popup_error(msg, title="Uh Oh!", icon=ICON_FILE_PATH)

    def enable_menu_item(self, menuElement, enable=True):
        for idx, el in enumerate(self.MENU_DEF):
            if menuElement in el:
                if enable:
                    self.MENU_DEF[idx][0] = '!' + self.MENU_DEF[idx][0]
                else:
                    self.MENU_DEF[idx][0] = self.MENU_DEF[idx][0].replace(
                        '!',
                        '')
                self._ui['menu'].update(self.MENU_DEF)
                break

            # print(self.MENU_DEF[idx], idx, menuElement)
        #         # self.MENU_DEF[idx]='!'+self.MENU_DEF[idx]
        #     break

    def clear_btn_pressed(self):
        self._ui[self.KEY_CONSOLE].update(value='')
        self._controller.clear_serial_rx_buffer()

    def open_project_file(self):
        filename = gui.popup_get_file('file to open',
                                      file_types=(('Porty Project (.prtyprj)',
                                                   '.prtyprj'),),
                                      no_window=True,
                                      icon=ICON_FILE_PATH)
        self._controller.open_project_settings(filename)
        self._msgList = self._controller.get_send_sequences()
        self._ui[self.KEY_MSG_LIST].update(values=self._msgList)
        self.set_port(self._controller.get_saved_port_name())

    def saveas_project_file(self):
        filename = gui.popup_get_file('file to Save',
                                      file_types=(('Porty Project (.prtyprj)',
                                                   '.prtyprj'),),
                                      save_as=True,
                                      no_window=True,
                                      icon=ICON_FILE_PATH)
        self._controller.save_project_settings(filename)

    def _debug_print_var(self, var):
        print(f'{var}')

    def launch(self):
        #  Setup Callbacks for connections
        self._controller.update_serial_cb(self.update_console,
                                          self.port_connected_cb,
                                          self.port_disconnected_cb)

        event, values = self._ui.read(timeout=10)
        self.refresh_port_list()
        while True:
            try:
                event, values = self._ui.read(timeout=10)
                if event in [gui.WIN_CLOSED, self.EV_MENU_QUIT]:
                    break
                elif event == self.KEY_REFRESH_PORT_LIST:
                    self.refresh_port_list()
                elif event == self.KEY_PORT_LIST:
                    self.set_port(values[self.KEY_PORT_LIST])
                elif event == self.KEY_OPEN_PORT:
                    if self._isConnected:
                        self.close_port_connection()
                    else:
                        self.open_port_connection()
                elif event == self.KEY_CLEAR_TERMINAL:
                    self.clear_btn_pressed()
                elif event == self.KEY_ADD_MSG_BTN:
                    self.update_msg_list(values[self.KEY_SEND_MSG_INPUT],
                                         True)
                elif event == self.KEY_REMOVE_MSG_BTN:
                    self.update_msg_list(values[self.KEY_SEND_MSG_INPUT],
                                         False)
                elif event == self.KEY_SEND_MSG_BTN:
                    self.send_msg(values[self.KEY_SEND_MSG_INPUT])
                elif event == self.KEY_MSG_LIST:
                    try:
                        self.update_send_msg_input(values[self.KEY_MSG_LIST][0])
                    except IndexError:
                        pass
                elif event == self.EV_MENU_OPEN_PROJECT:
                    self.open_project_file()
                elif event == self.EV_MENU_SAVE_AS_PROJECT:
                    self.saveas_project_file()
                elif event == self.EV_MENU_ABOUT:
                    self.about_popup()
                elif event in self.BAUD_RATES:
                    self._controller.update_port_baudrate(event)
                    # self._debug_print_var((event, values))
                if self._isConnected:
                    self._ui[self.KEY_PORT_LIST].update(disabled=True)
                    self._ui[self.KEY_OPEN_PORT].update(text='Close')
                    self._ui[self.KEY_SEND_MSG_BTN].update(disabled=False)
                else:
                    self._ui[self.KEY_PORT_LIST].update(disabled=False)
                    self._ui[self.KEY_OPEN_PORT].update(text='Open')
                    self._ui[self.KEY_SEND_MSG_BTN].update(disabled=True)
            except Exception as err:
                print(err)
                self.popup_error(err)

        # Finish up by removing from the screen
        self._ui.close()

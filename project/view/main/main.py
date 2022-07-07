import PySimpleGUI as gui
class MainUI:
    def __init__(self, title:str) -> None:
        # First the window layout in 2 columns
        conf_column = [
            [gui.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")],
        ]
        # For now will only show the name of the file that was chosen
        console_column = [
            [gui.Text("Console:")],
            [gui.Output(size=(80, 20), background_color='black', text_color='green')],
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
        while True:
            event, values = self._ui.read()
            # End program if user closes window or
            # presses the OK button
            if event == self._ui.WIN_CLOSED:
                break

        # Finish up by removing from the screen
        self._ui.close()
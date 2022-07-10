from .view import MainUI
from .controller import SerialController

class Project:
    def main(self):
        serialPort = SerialController()
        mainWindow = MainUI('Porty', serialPort)
        mainWindow.launch()
        
        
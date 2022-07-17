from .view import MainUI
from .controller import SerialController
from .model import MainModel

class Project:
    def main(self):
        mainModel = MainModel()
        serialPort = SerialController(mainModel)
        mainWindow = MainUI('Porty', serialPort)
        mainWindow.launch()
        
        
from project.controller.maincontroller import MainController
from .view import MainUI
from .model import MainModel

class Project:
    def main(self):
        mainModel = MainModel()
        mainController = MainController(mainModel)
        mainWindow = MainUI('Porty', mainController)
        mainWindow.launch()
        
        
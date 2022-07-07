from . import model, view, controller

class Project:
    def main(self):
        serialPort = controller.SerialController()
        mainWindow = view.MainUI('Porty')
        mainWindow.launch()
        
        
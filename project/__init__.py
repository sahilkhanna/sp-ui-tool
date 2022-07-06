from . import module, controller
class Project:
    def main(self):
        print(f'this is main {self}')
        sp = controller.SerialController()
        print(f'this is serialport {sp}')
        
        pass
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))
from project.controller.serialcontroller import SerialController, MainModel


def test_list_serial_ports(mocker):
    m = mocker.patch("project.controller.serialcontroller.list_ports.comports",
                     return_value=([('test1', None, None),
                                    ('test2', None, None)]))
    a = SerialController.list_serial_ports()
    assert type(a) == list
    assert a == ['test1', 'test2']
    assert a != ['test1']
    assert a != ['test2']


def test_set_comport(mocker):
    mocker.patch("project.controller.serialcontroller.MainModel.__init__",
                 return_value=None)
    mocker.patch("project.controller.serialcontroller.MainModel.get_all_port_settings",
                 return_value=None)
    mocker.patch("project.controller.serialcontroller.list_ports.comports",
                 return_value=([('test1', None, None),
                                ('test2', None, None)]))
    mdl = MainModel()
    sc = SerialController(mdl)
    sc.set_comport(comPortName='test1')
    assert sc._selectedPortName == 'test1'
    assert sc._selectedPortName != 'test2'

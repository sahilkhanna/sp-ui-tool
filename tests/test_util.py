import pytest
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))
from project.util import return_as_int


def test_return_as_int():
    x = return_as_int('1')
    assert x == 1
    assert x != '1'
    y = return_as_int(10)
    assert y == 10
    with pytest.raises(TypeError):
        return_as_int(b'\x02')

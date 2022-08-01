
def return_as_int(value) -> int:
    if type(value) == str:
        return int(value)
    elif type(value) == int:
        return value
    else:
        raise TypeError(f'Incorrect Baudrate type\
            {type(value)}')

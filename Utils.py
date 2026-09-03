import math

def Clamp(_value, _min, _max):
    return(min(_max, max(_min, _value)))

def Distance(_pointA, _pointB):
    dif = _pointA - _pointB
    return(dif.length())

def Sigmoid(_value):
    _value = max(-500, min(500, _value))
    return 1 / (1 + math.e ** (-_value))
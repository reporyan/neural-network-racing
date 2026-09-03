import pygame
import math

import Track
import Renderer

RETURN_CAR = True

class Raycast(object):
    def CastRange(self, _mask, _track, _origin, _direction, _car = None, _range = 1000, _step = 2, _stepChange = 0.02):
        stepDirection = _direction.normalize() * _step
        currentPosition = _origin.copy()
        range = 0
        step = _step
        
        #send raycast
        while range < _range:
            #increment
            currentPosition += stepDirection
            range += step
            step += _stepChange
            
            if(_mask != -1):
                #collision with TRACK
                #test surface here, this can be optimised by iterating only over surface
                surface = _track.PointOnTrack(currentPosition)
                if(surface[2] is _mask):
                    return range
            else:
                #collision with CARS
                car = _track.world.InCar(_car, currentPosition)
                if(car):
                    if(RETURN_CAR):
                        return car
                    else:
                        return range
        if(_mask != -1):
            return range
        else:
            return None
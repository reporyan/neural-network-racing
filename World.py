import copy
import math

from Car import Car
import Track
import pygame
from Training import Training

#consts
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

CAR_COLLISION_DISTANCE = 10

class World(object):
    def __init__(self):
        self.collisions = False

        self.mapIndex = 0
        self.mapCount = 2

        self.track = Track.Track(self)
        #self.cars = [Car(self, self.track.startPos, False)]
        self.cars = [Car(self, pygame.Vector2(40, 40), False)]
        self.training = Training(self)

        self.racing = False
        self.raceStatus = "In Progress"
        self.raceTimer = -1

    def Update(self, _deltaTime, _keys = None):
        if(self.racing == False):
            for car in self.cars:
                car.Update(_deltaTime, _keys)
            self.training.Update(_deltaTime, _keys)
        else:
            if(self.raceStatus == "In Progress"):
                self.raceTimer += _deltaTime
            if(self.raceTimer > 0):
                for car in self.cars:
                    car.Update(_deltaTime, _keys)
                    if(self.raceStatus == "In Progress"):
                        if(car.lastCheckpoint == len(self.track.checkPoints)):
                            if(car.isAI):
                                self.raceStatus = "AI Won!"
                            else:
                                self.raceStatus = "Player Won!"


    def InCar(self, _car, _point = None):
        if(_point is None):
            #this is not a raycast, real collision
            _point = _car.position
        #Raycast
        for car in self.cars:
            if(car != _car and (math.fabs(_point.x - car.position.x) <= CAR_COLLISION_DISTANCE and math.fabs(_point.y - car.position.y) <= CAR_COLLISION_DISTANCE)):
                return car
        return False

    def StartRace(self):
        self.racing = True
        self.raceTimer = -1
        self.raceStatus = "In Progress"

        if(self.collisions == False):
            self.cars = [self.cars[0], self.cars[1]]
            for car in self.cars:
                car.position = self.track.startPos.copy()
                car.direction = self.track.startDir
                car.speed = 0
                car.lastCheckpoint = -1
        
    def StopRace(self):
        self.racing = False
        self.raceTimer = -1

    def AddCar(self, _car):
        self.cars.append(_car)
    
    def RemoveCar(self, _car):
        self.cars.remove(_car)

    def RemoveAllCars(self):
        self.cars = []
    
    #hm...
    def RemoveAllAICars(self):
        self.cars = [self.cars[0]]



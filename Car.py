import pygame
import math
import time

import Renderer
import Utils
import NeuralNetwork
import Raycast

#do this later (clean)
ACCEL = 0.03
BRALE = 0.05
DRAG = 0.25
AXEL_OFFSET = 8

STEER_FORCE = 3
MAX_STEER_SPEED = 2
CORNERING = 0.5

DISTANCE_SCALER = 0.005
CAR_SENSE_SCALAR = 0.1

CAR_COLLISION_DRAG = 1

class Car(object):
    def __init__(self, _world, _position, _isAI = True):
        #track
        self.position = _position.copy()
        self.direction = _world.track.startDir

        self.speed = 0

        #control
        self.isAI = _isAI

        #const
        self.accel = 0.03
        self.brake = 0.05
        self.drag = 0.25#change based on surface
        self.axelOffset = 8

        self.steerForce = 3#change based on surface
        self.maxSteerSpeed = 2
        self.cornering = 0.5

        self.surface = None

        #render
        if(self.isAI):
            self.image = pygame.image.load("car.png").convert_alpha()
        else:
            self.image = pygame.image.load("player_car.png").convert_alpha()

        #ref
        self.track = _world.track
        self.world = _world
        self.raycast = Raycast.Raycast()
        self.distances = []

        #AI
        self.neuralNetwork = NeuralNetwork.NeuralNetwork()
        self.crashed = False#trial

        #AI reward
        self.lastCheckpoint = -1
        self.timeForLastCP = time.time()

    def Update(self, _deltaTime, _keys = None):
        #input
        #---surface---
        surface = self.track.PointOnTrack(self.position)

        if(not self.isAI):
            if(_keys is not None):
                if(_keys[pygame.K_w] or _keys[pygame.K_UP]):
                    self.speed += self.accel * _deltaTime * 60
                if(_keys[pygame.K_SPACE]):
                    self.speed -= self.brake
                    if(self.speed < 0):
                        self.speed = 0
                steerInput = 0
                if(_keys[pygame.K_d] or _keys[pygame.K_RIGHT]):
                    steerInput += 1
                if(_keys[pygame.K_a] or _keys[pygame.K_LEFT]):
                    steerInput -= 1
            
            steerInput = 0
        else:
            #---wall distances---
            wallDistances = []
            carDistances = []
            for i in range(-4, 5):
                angle = i * 18
                #add scaled distances
                wallDistances.append(self.raycast.CastRange(0, self.track, self.position, pygame.Vector2(math.cos(math.radians(self.direction + angle)), math.sin(math.radians(self.direction + angle)))) * DISTANCE_SCALER)
            
            #---car collision distances---
            if(len(self.neuralNetwork.layers[0]) > 12):
                for i in range(8):
                    angle = i * 45
                    #add scaled distances
                    #carDistances.append(self.raycast.CastRange(-1, self.track, self.position, pygame.Vector2(math.cos(math.radians(self.direction + angle)), math.sin(math.radians(self.direction + angle))), self, 100) * DISTANCE_SCALER)
                    otherCar = self.raycast.CastRange(-1, self.track, self.position, pygame.Vector2(math.cos(math.radians(self.direction + angle)), math.sin(math.radians(self.direction + angle))), self, 100)
                    if(otherCar):
                        carDistances.append((otherCar.speed - self.speed) * CAR_SENSE_SCALAR)
                    else:
                        carDistances.append(0)
            
            #gather inputs, 0 is accel, 1 is brake, 2 is right, 3 is left
            input = self.neuralNetwork.Process(wallDistances + [self.speed] + [surface[0]] + [surface[1]] + carDistances)
            if(input[0] > 0.5):
                self.speed += self.accel * _deltaTime * 60
            if(input[1] > 0.5):
                self.speed -= self.brake
                if(self.speed < 0):
                    self.speed = 0
            steerInput = 0
            if(input[2] > 0.5):
                steerInput += 1
            if(input[3] > 0.5):
                steerInput -= 1

            #debug
            #use NN
            self.distances = wallDistances

        #drag
        self.speed *= max(1 - surface[0] * _deltaTime, 0)

        #debug
        self.surface = surface

        #steering
        steerOutput = self.SteeringForce(surface[1], self.steerForce, steerInput, self.speed, self.cornering, self.maxSteerSpeed)
        self.direction += steerOutput * _deltaTime * 60

        #crash into wall
        if(surface[2] == 0):
            self.crashed = True

        #collision with other cars
        if(self.world.collisions and self.world.InCar(self)):
            self.speed *= max(1 - CAR_COLLISION_DRAG * _deltaTime, 0)
        
        #move (apply velo)
        self.position.x += math.cos(math.radians(self.direction)) * self.speed * _deltaTime * 60
        self.position.y += math.sin(math.radians(self.direction)) * self.speed * _deltaTime * 60

        #reward
        #if we are at the next checkpoint, increase our last checkpoint
        if(self.track.PointInCheckpoint(self.position) == ((self.lastCheckpoint + 1) % len(self.track.checkPoints))):
            self.lastCheckpoint += 1
            self.timeForLastCP = time.time()

    def SteeringForce(self, _surface, _force, _input, _speed, _cornering, _maxSteerSpeed):
        if(_speed == 0):
            return 0
        _input = Utils.Clamp(_input, -1, 1)
        if(_speed <= _maxSteerSpeed):
            return _surface * _force * (_speed / _maxSteerSpeed) * _input
        return (_surface * _force * _cornering * _input) / ((_speed / _maxSteerSpeed) + _cornering - 1)
    
    def Reward(self):
        reward = 0
        reward += self.lastCheckpoint
        reward += Utils.Sigmoid((time.time() - self.timeForLastCP) / 5)#divide so that it doesn't go super low
        return reward


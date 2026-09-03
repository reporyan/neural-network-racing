from Car import Car
import Track
import pygame
import math

#--- consts; edit these to affect training ---

#how many cars are in each generation. Many cars can be good for finding new paths and greatly increases variance. This also affects collision races.
GENERATION_POPULATION = 15

#how long before each generation is ended. longer gets a more accurate representation, but.. takes longer. Ideally all cars should be able to show what they can do in this time.
GENERATION_TIME = 15

#Biases are very important. Too high and cars don't care about the last generation winner, too low and they are scared to try new things. Note: these use bell curve distributions, and are also affected by reward.
#how much node weights are changed each generation. Each node has weights for all nodes in the next layer.
WEIGHT_VARIENCE = 3

#how much node biases are changed each generation. Each node has a single bias.
BIAS_VARIENCE = 3

TRAINING_AI = True

class Training(object):
    def __init__(self, _world):
        self.world = _world

        self.timer = 0
        self.generation = 1
        self.bestScore = -999

        if(TRAINING_AI):
            for i in range(GENERATION_POPULATION):
                car = self.NewCar(i)
                self.world.AddCar(car)   
        
        self.bestCar = self.world.cars[1]#account for player

    def Update(self, _deltaTime, _keys = None):
        if(TRAINING_AI):
            #AI
            self.timer += _deltaTime

            #trial
            foundSafe = False
            for car in self.world.cars:
                if(not car.crashed and car.isAI):
                    foundSafe = True
                    break
            
            #when time is up
            if(self.timer >= GENERATION_TIME or not foundSafe):
                self.NextGeneration()

    def NextGeneration(self):
        self.generation += 1

        #find car with best score, must be bigger than global best score
        for car in self.world.cars:
            if(not car.isAI):
                continue
            reward = car.Reward()
            if(reward > self.bestScore):
                self.bestScore = reward
                self.bestCar = car

        weightVariance = WEIGHT_VARIENCE / (self.bestScore + 1.5)
        biasVariance = BIAS_VARIENCE / (self.bestScore + 1.5)

        #delete all cars for new generation
        self.world.RemoveAllAICars()

        #add new generation mutated based on best
        for i in range(GENERATION_POPULATION):
            car = self.NewCar(i)
            car.neuralNetwork = self.bestCar.neuralNetwork.DeepCopy()
            if(i > 0):
                car.neuralNetwork.ChangeRandomise(biasVariance, weightVariance)
            self.world.AddCar(car)

        self.timer = 0

    def NewCar(self, _i):
        if(self.world.collisions):
            startVec = pygame.Vector2(math.cos(math.radians(self.world.track.startDir)), math.sin(math.radians(self.world.track.startDir))).normalize()
            perpVec = pygame.Vector2(-startVec.y, startVec.x)
            return Car(self.world, self.world.track.startPos + (startVec * _i * -25) + (perpVec * ((_i % 2) - 0.5) * 25), True)
        else:
            return Car(self.world, self.world.track.startPos, True)
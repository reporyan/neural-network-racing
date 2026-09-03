import pygame
import math
from enum import Enum
import Utils

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

NN_VISUAL_COLOUR_SCALAR = 100
NN_VISUAL_COLOUR_OFFSET = 128

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#put this back
alphaScreen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

class DebugMode(Enum):
    GENERATION_STATS = 0,
    CAR_NN = 1,
    CAR_STEER = 2

class Renderer(object):
    def __init__(self):
        self.world = None
        self.training = None
        self.font = pygame.font.SysFont("Ariel", 16)
        self.renderIndex = 1#but must account for player

        self.debugMode = DebugMode.GENERATION_STATS
        self.showScores = False
        self.renderCheckpoints = False

    def NNToScreen(self, _layer, _row, _layerCount, _rowCount):
        return pygame.Vector2(725 + _layer * 225 / (_layerCount - 1), 350 + (_row - _rowCount / 2) * 20)
    
    def Render(self, _deltaTime, _time, _collision, _headless):
        #clear everything
        screen.fill((50, 50, 50))
        alphaScreen.fill((0, 0, 0, 0))
        self.font = pygame.font.SysFont("Ariel", 16)

        #track
        if(self.world.track != None):
            #rectangles
            if(len(self.world.track.roadRectangles) > 0):#do we have to do this?
                for rect in self.world.track.roadRectangles:
                    pygame.draw.rect(screen, (100, 100, 100), rect)

            #rectangles
            if(len(self.world.track.dirtRectangles) > 0):
                for rect in self.world.track.dirtRectangles:
                    pygame.draw.rect(screen, (150, 125, 100), rect)

            #rectangles
            if(len(self.world.track.grassRectangles) > 0):
                for rect in self.world.track.grassRectangles:
                    pygame.draw.rect(screen, (100, 150, 100), rect)

            #circles
            if(len(self.world.track.roadCircles) > 0):
                for circle in self.world.track.roadCircles:
                    pygame.draw.circle(screen, (100, 100, 100), (circle[0], circle[1]), circle[2])
            
            #circles
            if(len(self.world.track.dirtCircles) > 0):
                for circle in self.world.track.dirtCircles:
                    pygame.draw.circle(screen, (150, 125, 100), (circle[0], circle[1]), circle[2])

            #circles
            if(len(self.world.track.grassCircles) > 0):
                for circle in self.world.track.grassCircles:
                    pygame.draw.circle(screen, (100, 150, 100), (circle[0], circle[1]), circle[2])

            #checkpoints
            if(self.renderCheckpoints and len(self.world.track.checkPoints) > 0):
                for i in range(len(self.world.track.checkPoints)):
                    rect = self.world.track.checkPoints[i]
                    pygame.draw.rect(alphaScreen, (255, 255, 0, 75), rect, 4)
                    surface = self.font.render((f"CP{i}"), True, (255, 255, 0))
                    screen.blit(surface, pygame.Vector2(rect.x + 10, rect.y + 10))

        #draw alpha before cars
        screen.blit(alphaScreen, (0, 0))

        #draw debug panel
        pygame.draw.rect(screen, (30, 30, 30), (700, 0, 300, 600))
        pygame.draw.rect(screen, (100, 100, 100), (700, 110, 300, 10))
        self.font = pygame.font.SysFont("Ariel", 32)

        #generation
        if(self.debugMode == DebugMode.GENERATION_STATS):
            colour = (0, 255, 0)
        else:
            colour = (255, 255, 255)
        surface = self.font.render(f"[1] Generation", True, colour)
        screen.blit(surface, pygame.Vector2(725, 25))

        #car neural network
        if(self.debugMode == DebugMode.CAR_NN):
            colour = (0, 255, 0)
        else:
            colour = (255, 255, 255)
        surface = self.font.render(f"[2] Car Neural Network", True, colour)
        screen.blit(surface, pygame.Vector2(725, 50))

        #steering
        if(self.debugMode == DebugMode.CAR_STEER):
            colour = (0, 255, 0)
        else:
            colour = (255, 255, 255)
        surface = self.font.render(f"[3] Car Steering", True, colour)
        screen.blit(surface, pygame.Vector2(725, 75))

        #generation
        if(self.debugMode == DebugMode.GENERATION_STATS):
            self.font = pygame.font.SysFont("Ariel", 32)
            surface = self.font.render((f"Generation: {self.training.generation}"), True, (255, 255, 0))
            screen.blit(surface, pygame.Vector2(725, 125))
            surface = self.font.render((f"Gen Timer: {round(self.training.timer, 3)}"), True, (255, 255, 0))
            screen.blit(surface, pygame.Vector2(725, 150))
            surface = self.font.render((f"Best Reward: {round(self.training.bestScore, 3)}"), True, (255, 255, 0))
            screen.blit(surface, pygame.Vector2(725, 175))
            surface = self.font.render((f"Headless: {_headless}"), True, (200, 0, 100))
            screen.blit(surface, pygame.Vector2(725, 225))
            surface = self.font.render((f"Headless Time: {_time}"), True, (200, 0, 100))
            screen.blit(surface, pygame.Vector2(725, 250))
            surface = self.font.render((f"Collisions: {_collision}"), True, (100, 0, 255))
            screen.blit(surface, pygame.Vector2(725, 300))

        if(self.world.racing):
            lights = max(round(0 - self.world.raceTimer * 5), 0)
            for i in range(lights):
                    pygame.draw.circle(screen, (255, 0, 0), (100 + i * 24, 25), 10)
            surface = self.font.render(f"Race Time: {round(self.world.raceTimer, 3)}", True, (255, 0, 0))
            screen.blit(surface, pygame.Vector2(250, 15))
            surface = self.font.render(f"{self.world.raceStatus}", True, (255, 0, 0))
            screen.blit(surface, pygame.Vector2(500, 15))

        #cars
        self.font = pygame.font.SysFont("Ariel", 16)
        if(len(self.world.cars) > 0):
            for i in range(len(self.world.cars)):
                car = self.world.cars[i]

                #rotate car
                rotatedCar = pygame.transform.rotate(car.image, -car.direction)

                #offset
                offset = pygame.Vector2(math.cos(math.radians(car.direction)), math.sin(math.radians(car.direction))) * car.axelOffset
                
                #render car
                carRect = rotatedCar.get_rect(center = (car.position.x, car.position.y) + offset)
                screen.blit(rotatedCar, carRect)

                #debug
                if(self.debugMode == DebugMode.CAR_NN):
                    #circle
                    if(i == self.renderIndex):
                        colour = (255, 0, 0)
                    else:
                        colour = (0, 255, 0)

                    pygame.draw.circle(screen, colour, car.position, 2)

                    if(i == self.renderIndex):
                        for i in range(-4, 5):
                            angle = i * 18
                            endPos = car.position + pygame.Vector2(math.cos(math.radians(car.direction + angle)) * car.neuralNetwork.layers[0][i + 4].value / 0.005, math.sin(math.radians(car.direction + angle)) * car.neuralNetwork.layers[0][i + 4].value / 0.005)
                            pygame.draw.line(screen, (0, 255, 0), car.position, endPos)
                        if(len(car.neuralNetwork.layers[0]) > 12):
                            for i in range(8):
                                angle = i * 45
                                endPos = car.position + pygame.Vector2(math.cos(math.radians(car.direction + angle)) * car.neuralNetwork.layers[0][i + 12].value / 0.005, math.sin(math.radians(car.direction + angle)) * car.neuralNetwork.layers[0][i + 12].value / 0.005)
                                pygame.draw.line(screen, (255, 255, 0), car.position, endPos)

                    #neural network
                    if(len(self.world.cars) <= self.renderIndex):
                        continue

                    surface = self.font.render(f"Watching Car: {self.renderIndex}", True, (0, 255, 0))
                    screen.blit(surface, pygame.Vector2(720, 125))

                    neuralNetwork = self.world.cars[self.renderIndex].neuralNetwork
                    for i in range(len(neuralNetwork.layers)):
                        for j in range(len(neuralNetwork.layers[i])):
                            #what to display
                            surface = self.font.render(str(round(neuralNetwork.layers[i][j].value, 2)), True, (255, 255, 255))
                            
                            #position on screen
                            position = self.NNToScreen(i, j, len(neuralNetwork.layers), len(neuralNetwork.layers[i]))

                            #lines
                            if(i < len(neuralNetwork.layers) - 1):
                                for k in range(len((neuralNetwork.layers[i + 1]))):
                                    endPosition = self.NNToScreen(i + 1, k, len(neuralNetwork.layers), len(neuralNetwork.layers[i + 1]))
                                    colour = Utils.Clamp(round(neuralNetwork.layers[i][j].weights[k] * neuralNetwork.layers[i][j].value * NN_VISUAL_COLOUR_SCALAR + NN_VISUAL_COLOUR_OFFSET), 0, 255)
                                    pygame.draw.line(screen, (0, colour, 0),position + (10, 10), endPosition + (10, 10))
 
                            pygame.draw.circle(screen, (0, 0, Utils.Clamp(round(neuralNetwork.layers[i][j].value  * 255), 0, 255)), position + (10, 10), 8)
                            screen.blit(surface, position)
                            
                            

                if(self.debugMode == DebugMode.CAR_STEER):
                    #debug steer graph
                    if(i == self.renderIndex and car.surface):
                        print(700 + car.speed * 10)
                        for j in range(600):
                            pygame.draw.circle(screen, (0, 255, 0), pygame.Vector2(j/2 + 700, SCREEN_HEIGHT - 100 * car.SteeringForce(car.surface[1], car.steerForce, 1, j / 100, car.cornering, car.maxSteerSpeed)), 2)
                            pygame.draw.circle(screen, (255, 0, 0), pygame.Vector2(car.speed/2 * 100 + 700, SCREEN_HEIGHT - 100 * car.SteeringForce(car.surface[1], car.steerForce, 1, car.speed, car.cornering, car.maxSteerSpeed)), 8)

                if(self.showScores):
                    #score
                    surface = self.font.render(str(round(car.Reward(), 2)), True, (255, 255, 255))
                    screen.blit(surface, car.position)

        #other labels
        #FPS
        self.font = pygame.font.SysFont("Ariel", 32)
        surface = self.font.render("FPS: " + str(round(1 / _deltaTime)), True, (100, 100, 100))
        screen.blit(surface, pygame.Vector2(10, 575))

        pygame.display.flip()


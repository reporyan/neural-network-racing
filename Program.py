import sys
import time
import math
import pygame

import Car
import Renderer
import World

headless = False
renderHeadless = False
FPS = 60
TRAINING_FPS = 60
DEBUG_INTERVAL = 60

running = True

previousKeys = None

#time
clock = pygame.time.Clock()
prevTime = time.time() - 0.01
startTime = time.time()
deltaTime = 0.016
frames = 0

#pygame
pygame.init()

#references
renderer = Renderer.Renderer()
world = World.World()

#renderer references
renderer.world = world
renderer.training = world.training
training = world.training

def QueryDebugKey(_key):
    return (keys[_key] and not previousKeys[_key])

def LoadAllNN(_filename):
    for car in world.cars:
        if(car.isAI):
            car.neuralNetwork.LoadFromFile(f"{_filename}.txt")
    training.bestCar = world.cars[1]
    print(f"--- Loading Neural Network File: {_filename} ---")

if(__name__ == "__main__"):
    print(sys.argv)
    print("=== PROGRAM STARTED ===")

#running and rendering
while(running):
    #input
    keys = pygame.key.get_pressed()
    keysDown = []
    for key in keys:
        keysDown.append(QueryDebugKey(key))

    if(QueryDebugKey(pygame.K_h)):
        headless = not headless
        clock.tick()

    #training
    if (headless):
        deltaTime = 1 / TRAINING_FPS

        world.Update(deltaTime)

        #if(renderHeadless):
            #renderer.Render(deltaTime)

        if(frames % DEBUG_INTERVAL == 0):
            print("--- Training AI! ---")
            print(f"Time: {round(frames / TRAINING_FPS, 2)}s")
            print("Generation: " + str(training.generation))
            print("Best Score: " + str(round(training.bestScore, 5)))

            #for debug stats
            renderer.Render(deltaTime, round(frames / TRAINING_FPS, 2), world.collisions, headless)

        frames += 1
    else:
        #delta time
        deltaTime = clock.tick(FPS) / 1000
        #print(f"Delta Time: {deltaTime}")
        
        #update
        world.Update(deltaTime, keys)

        renderer.Render(deltaTime, round(frames / TRAINING_FPS, 2), world.collisions, headless)

    #print(f"Delta Time: {deltaTime}")

    #debug mode, also add in array at top
    if(QueryDebugKey(pygame.K_1)): renderer.debugMode = Renderer.DebugMode.GENERATION_STATS
    if(QueryDebugKey(pygame.K_2)): renderer.debugMode = Renderer.DebugMode.CAR_NN
    if(QueryDebugKey(pygame.K_3)): renderer.debugMode = Renderer.DebugMode.CAR_STEER

    #toggle reward debug
    if(QueryDebugKey(pygame.K_r)): renderer.showScores = not renderer.showScores

    #save and load
    if(QueryDebugKey(pygame.K_s)):
        world.training.bestCar.neuralNetwork.SaveToFile("NeuralNetworkSave.txt")
        print("--- Saving Best Car NN To File ---")
    
    if(QueryDebugKey(pygame.K_l)):
        world.training.NextGeneration()
        LoadAllNN("NeuralNetworkSave")

    #collision
    if(QueryDebugKey(pygame.K_c)): world.collisions = not world.collisions
    
    #skip gen
    if(QueryDebugKey(pygame.K_n)):
        world.StopRace()
        world.training.NextGeneration() 

    #checkpoints
    if(QueryDebugKey(pygame.K_p)): renderer.renderCheckpoints = not renderer.renderCheckpoints

    if(QueryDebugKey(pygame.K_d)):
        if(not world.racing):
            world.StartRace()
        else:
            world.StopRace()

    #DEMOS
    if(QueryDebugKey(pygame.K_0)):
        world.track.LoadRawTrack(0)
        world.training.NextGeneration()
        LoadAllNN("10x4NN")

    if(QueryDebugKey(pygame.K_9)):
        world.track.LoadRawTrack(0)
        world.training.NextGeneration()
        LoadAllNN("10x4x4NN")
    
    if(QueryDebugKey(pygame.K_8)):
        world.track.LoadRawTrack(1)
        world.training.NextGeneration()
        LoadAllNN("12x4_terrainNN")

    if(QueryDebugKey(pygame.K_7)):
        world.track.LoadRawTrack(1)
        world.training.NextGeneration()
        LoadAllNN("12x4x4_terrainNN")

    if(QueryDebugKey(pygame.K_6)):
        world.track.LoadRawTrack(1)
        world.training.NextGeneration()
        LoadAllNN("Collision")

    #cycle debug index
    if(QueryDebugKey(pygame.K_COMMA)):
        renderer.renderIndex -= 1
        renderer.renderIndex = renderer.renderIndex % len(world.cars)

    if(QueryDebugKey(pygame.K_PERIOD)):
        renderer.renderIndex += 1
        renderer.renderIndex = renderer.renderIndex % len(world.cars)

    #map cycle
    if(QueryDebugKey(pygame.K_m)):
        if(keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
            world.track.LoadTrack("TrackSave.txt")
            world.training.NextGeneration()
        else:
            world.mapIndex += 1
            world.mapIndex =  world.mapIndex % world.mapCount
            world.track.LoadRawTrack(world.mapIndex)
            world.training.NextGeneration()

    #set prev keys
    previousKeys = keys

    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


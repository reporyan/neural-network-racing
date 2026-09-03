import pygame
import Utils

TRACK_WIDTH = 6
TRACK_HEIGHT = 5

surfaces = {
    #Drag, Steer, ID for raycast
    "Wall": (10, 1, 0),
    "Road": (0.2, 1, 1),
    "Dirt": (1.2, 0.6, 2),
    "Grass": (0.5, 0.3, 3)
}

#may need to use my own classes, to define wider corners
class Track(object):
    def __init__(self, _world):
        self.world = _world

        self.roadRectangles = []
        self.dirtRectangles = []
        self.grassRectangles = []
        self.roadCircles = []

        #SWAP TRACK HERE FOR NOW
        #self.LoadTrack("dirt_grass.txt")
        self.LoadRawTrack(self.world.mapIndex)
                
    #checks if a point is inside the track
    def PointOnTrack(self, _point):
        #in rect
        for rect in self.roadRectangles:
            if(_point.x >= rect.x and _point.x <= rect.x + rect.w and _point.y >= rect.y and _point.y <= rect.y + rect.h):
                return surfaces["Road"]
        
        #in rect
        for rect in self.dirtRectangles:
            if(_point.x >= rect.x and _point.x <= rect.x + rect.w and _point.y >= rect.y and _point.y <= rect.y + rect.h):
                return surfaces["Dirt"]

        #in rect
        for rect in self.grassRectangles:
            if(_point.x >= rect.x and _point.x <= rect.x + rect.w and _point.y >= rect.y and _point.y <= rect.y + rect.h):
                return surfaces["Grass"]

        #in circle
        for circle in self.roadCircles:
            if(Utils.Distance(pygame.Vector2(circle[0], circle[1]), _point) <= circle[2]):
                return surfaces["Road"]
            
        #in circle
        for circle in self.dirtCircles:
            if(Utils.Distance(pygame.Vector2(circle[0], circle[1]), _point) <= circle[2]):
                return surfaces["Dirt"]
            
        #in circle
        for circle in self.grassCircles:
            if(Utils.Distance(pygame.Vector2(circle[0], circle[1]), _point) <= circle[2]):
                return surfaces["Grass"]
    
        return surfaces["Wall"]
    
    def PointInCheckpoint(self, _point):
        #in checkpoint
        for i in range(len(self.checkPoints)):
            if(_point.x >= self.checkPoints[i].x and _point.x <= self.checkPoints[i].x + self.checkPoints[i].w and _point.y >= self.checkPoints[i].y and _point.y <= self.checkPoints[i].y + self.checkPoints[i].h):
                return i
        #returns the index of checkpoint the _point is in
        return -1
    
    def LoadRawTrack(self, _index):
        self.roadRectangles = []
        self.dirtRectangles = []
        self.grassRectangles = []
        self.roadCircles = []
        self.dirtCircles = []
        self.grassCircles = []
        
        if(_index == 0):
            self.startPos = pygame.Vector2(100, 400)
            self.startDir = 90
            

            self.roadRectangles = [pygame.Rect(50, 100, 100, 400),
                            pygame.Rect(100, 450, 200, 100),
                            pygame.Rect(250, 300, 100, 200),
                            pygame.Rect(300, 250, 300, 100),
                            pygame.Rect(550, 100, 100, 200),
                            pygame.Rect(100, 50, 500, 100)]
            self.roadCircles = [(100, 100, 50),
                            (100, 500, 50),
                            (300, 500, 50),
                            (300, 300, 50),
                            (600, 300, 50),
                            (600, 100, 50)]
            self.checkPoints = [pygame.Rect(50, 450, 100, 100),
                                pygame.Rect(150, 450, 100, 100),
                                pygame.Rect(250, 450, 100, 100),
                                pygame.Rect(250, 350, 100, 100),
                                pygame.Rect(250, 250, 100, 100),
                                pygame.Rect(350, 250, 100, 100),
                                pygame.Rect(450, 250, 100, 100),
                                pygame.Rect(550, 250, 100, 100),
                                pygame.Rect(550, 150, 100, 100),
                                pygame.Rect(550, 50, 100, 100),
                                pygame.Rect(450, 50, 100, 100),
                                pygame.Rect(350, 50, 100, 100),
                                pygame.Rect(250, 50, 100, 100),
                                pygame.Rect(150, 50, 100, 100),
                                pygame.Rect(50, 50, 100, 100),
                                pygame.Rect(50, 150, 100, 100),
                                pygame.Rect(50, 250, 100, 100),
                                pygame.Rect(50, 350, 100, 100),]
        if(_index == 1):
            self.startPos = pygame.Vector2(100, 200)
            self.startDir = 270

            self.roadRectangles = [pygame.Rect(50, 100, 100, 300),
                            pygame.Rect(100, 50, 200, 100),
                            pygame.Rect(100, 350, 100, 100),
                            pygame.Rect(150, 400, 100, 50)]
            self.roadCircles = [(100, 100, 50),
                            (100, 400, 50),
                            (200, 400, 50)]
            self.dirtRectangles = [pygame.Rect(150, 450, 100, 50),
                                pygame.Rect(200, 450, 400, 100),
                                pygame.Rect(550, 300, 100, 200),
                                pygame.Rect(500, 250, 100, 100)]
            self.dirtCircles = [(200, 500, 50),
                                (600, 500, 50),
                                (600, 300, 50)]
            self.grassRectangles = [pygame.Rect(450, 250, 50, 100),
                                    pygame.Rect(400, 100, 100, 200),
                                    pygame.Rect(300, 50, 150, 100)]
            self.grassCircles = [(450, 300, 50),
                                 (450, 100, 50)]
            self.checkPoints = [pygame.Rect(50, 50, 100, 100),
                                pygame.Rect(150, 50, 100, 100),
                                pygame.Rect(250, 50, 100, 100),
                                pygame.Rect(350, 50, 50, 100),
                                pygame.Rect(400, 50, 100, 100),
                                pygame.Rect(400, 150, 100, 100),
                                pygame.Rect(400, 250, 100, 100),
                                pygame.Rect(500, 250, 50, 100),
                                pygame.Rect(550, 250, 100, 100),
                                pygame.Rect(550, 350, 100, 100),
                                pygame.Rect(550, 450, 100, 100),
                                pygame.Rect(450, 450, 100, 100),
                                pygame.Rect(350, 450, 100, 100),
                                pygame.Rect(250, 450, 100, 100),
                                pygame.Rect(150, 450, 100, 100),
                                pygame.Rect(150, 350, 100, 100),
                                pygame.Rect(50, 350, 100, 100),
                                pygame.Rect(50, 250, 100, 100),
                                pygame.Rect(50, 150, 100, 100)]

    def LoadTrack(self, _filename):
        self.roadRectangles = []
        self.dirtRectangles = []
        self.grassRectangles = []
        self.roadCircles = []
        self.dirtCircles = []
        self.grassCircles = []

        with open(_filename, "r") as file:
            lines = file.readlines()
            x = 0
            y = 0
            self.roadRectangles = []
            self.dirtRectangles = []
            self.grassRectangles = []
            self.circles = []
            self.checkPoints = []

            indexedCheckPoints = []
            cpCount = 0

            while (y < TRACK_HEIGHT):
                #tile is type
                tile = lines[y][(x * 3)]

                #cp num is checkpoint number if applicable
                cpNum = lines[y][(x * 3) + 1] + lines[y][(x * 3) + 2]

                #checkpoint
                if(cpNum != ".."):
                    worldPos = self.CoordToScreenTopLeft(x, y)
                    indexedCheckPoints.append((cpNum, pygame.Rect(worldPos.x, worldPos.y, 100, 100)))
                    cpCount += 1

                #tile
                if(tile == "r"):
                    self.roadRectangles.append(pygame.Rect(worldPos.x, worldPos.y, 100, 100))
                if(tile == "d"):
                    self.dirtRectangles.append(pygame.Rect(worldPos.x, worldPos.y, 100, 100))
                if(tile == "g"):
                    self.grassRectangles.append(pygame.Rect(worldPos.x, worldPos.y, 100, 100))
                if(tile == "s"):
                    self.roadRectangles.append(pygame.Rect(worldPos.x, worldPos.y, 100, 100))
                    self.start = self.CoordToScreenCentre(x, y)
                    self.startDir = 270
                
                x += 1
                if(x >= TRACK_WIDTH):
                        x = 0
                        y += 1

            #order checkpoints
            indexedCheckPoints.sort()
            for indexedCP in indexedCheckPoints:
                self.checkPoints.append(indexedCP[1])
                print(indexedCP[0])

            #start finish dir pos
            self.startPos = self.CoordToScreenCentre(int(lines[TRACK_HEIGHT]), int(lines[TRACK_HEIGHT + 1]))
            self.startDir = int(lines[TRACK_HEIGHT + 2])

    def CoordToScreenTopLeft(self, _x, _y):
        return pygame.Vector2(50 + _x * 100, 50 + _y * 100)
    
    def CoordToScreenCentre(self, _x, _y):
        return pygame.Vector2(100 + _x * 100, 100 + _y * 100)
    


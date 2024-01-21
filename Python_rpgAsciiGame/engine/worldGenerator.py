import random
from tiles.roomTile import RoomTile
from tiles.roadTile import RoadTile
from tiles.wallTile import WallTile
from tiles.playerTile import PlayerTile
from colors.colorPalettes import *

class WorldGenerator:
    def __init__(self, x=50, y=50, rooms=20):
        self.roomSizes = (7,9,11,13,15) #odd numbers so rooms they are going to have center
        self.xSize = x
        self.ySize = y
        self.numRooms = rooms
        self.world = []
        self.roomOrigins = []
        self.player = None

        self.createWorld()


    def createWorld(self):
        self.world = [
            [
                WallTile(hitPoints=-1, xyPoz=(x, 0)) if y == 0 or y == self.ySize - 1 or x == 0 or x == self.xSize - 1
                else WallTile(xyPoz=(x, y))
                for x in range(self.xSize)
            ]
            for y in range(self.ySize)
        ]

        # self.world = [[WallTile(hitPoints=-1)]+([WallTile()] * (self.xSize-2))+[WallTile(hitPoints=-1)] for _ in range(self.ySize-2)]
        # self.world.insert(0,[WallTile(hitPoints=-1)] * self.xSize)
        # self.world.append([WallTile(hitPoints=-1)] * self.xSize)
        self.placePoints()
        self.createRoads()
        self.createPlayer()



    def placePoints(self):
        roomCount = 1
        for i in range(self.numRooms):
            xPoint, yPoint = self.pickRandomPoint()
            diameter = self.roomSizes[random.randrange(len(self.roomSizes))]

            while not self.checkForRoom((xPoint, yPoint),diameter):
                diameter = self.roomSizes[random.randrange(len(self.roomSizes))]
                xPoint, yPoint = self.pickRandomPoint()

            self.world[yPoint][xPoint] = RoomTile(roomCount, xyPoz=(xPoint,yPoint))
            self.world[yPoint][xPoint].setCenter(True)
            self.roomOrigins.append((xPoint, yPoint))
            self.createRoom((xPoint, yPoint),roomCount,diameter)
            roomCount += 1

    def createRoom(self, xyPoz, roomId,diameter):

        radius = diameter // 2
        r_squared = radius ** 2

        xOffset = xyPoz[0] - radius
        yOffset = xyPoz[1] - radius

        for i in range(diameter):
            y = (i - radius) ** 2
            for j in range(diameter):
                x = (j - radius) ** 2
                if x + y <= r_squared and (xOffset > 0 and xOffset < self.xSize-1) and (yOffset > 0 and yOffset < self.ySize-1):
                    if self.world[yOffset][xOffset].getTileId() > 0:
                        self.world[yOffset][xOffset] = RoomTile(roomId=roomId,diameter=diameter,xyPoz=(xOffset,yOffset))

                xOffset += 1
            xOffset = xyPoz[0] - radius
            yOffset += 1

    def checkForRoom(self, xyPoz,diameter):
        radius = diameter // 2
        r_squared = radius ** 2

        xOffset = xyPoz[0] - radius
        yOffset = xyPoz[1] - radius
        canCreate = True

        for i in range(diameter):
            y = (i - radius) ** 2
            for j in range(diameter):
                x = (j - radius) ** 2
                if x + y <= r_squared and (xOffset > 0 and xOffset < self.xSize - 1) and (yOffset > 0 and yOffset < self.ySize - 1) and self.world[yOffset][xOffset].getTileId() < 0:
                    canCreate = False
                    break
                xOffset += 1
            xOffset = xyPoz[0] - radius
            yOffset += 1
        return canCreate

    def connectRooms(self,point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        line1 = [(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)]
        line2 = [(x2, y) for y in range(min(y1, y2), max(y1, y2) + 1)]

        connectedLine = line1 + line2

        return connectedLine

    def connectAllRooms(self):
        connectedLines = []
        for i in range(len(self.roomOrigins) - 1):
            connectedLines.extend(self.connectRooms(self.roomOrigins[i], self.roomOrigins[i + 1]))
        return connectedLines

    def createRoads(self):
        connectionLines = self.connectAllRooms()
        for y in range(self.ySize):
            for x in range(self.xSize):
                if (x, y) in connectionLines and self.world[y][x].getTileId() > 0:
                    self.world[y][x] = RoadTile(xyPoz=(x,y))

    def createPlayer(self):
        randomRoom = random.choice(self.roomOrigins)
        self.player = PlayerTile(xyPoz=randomRoom)
        room = self.world[randomRoom[1]][randomRoom[0]]
        self.player.setStandingTile(room)
        self.world[randomRoom[1]][randomRoom[0]] = self.player

    def getXSize(self):
        return self.xSize

    def getYSize(self):
        return self.ySize

    def pickRandomPoint(self):
        return random.randrange(1, self.xSize-1), random.randrange(1, self.ySize-1)

    def getWorld(self):
        return self.world

    def getPlayer(self):
        return self.player

    def getPlayerPoz(self):
        return self.player.getTilePoz()

    def showWorldMap(self):
        for line in self.world:
            for tile in line:
                print(tile.getTileFgColor(),tile.getTileChar(),end="")
            print()

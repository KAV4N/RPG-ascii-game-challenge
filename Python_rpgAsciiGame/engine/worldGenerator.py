import random
from tiles.roomTile import RoomTile
from tiles.roadTile import RoadTile
from tiles.wallTile import WallTile
from tiles.playerTile import PlayerTile
from colors.colorPalettes import *
from engine.threadSafeList import ThreadSafeList

class WorldGenerator:
    def __init__(self, x=50, y=50, rooms=20):
        self.roomSizes = (7,9,11,13,15) #odd numbers so rooms they are going to have center
        self.xSize = x
        self.ySize = y
        self.numRooms = rooms
        self.world = None
        self.roomOrigins = []
        self.player = None
        self.createWorld()


    def createWorld(self):
        self.world = ThreadSafeWorld(self.xSize, self.ySize)
        self.placePoints()
        self.createRoads()
        self.createPlayer()



    def placePoints(self):
        roomCount = 1
        while self.numRooms >= roomCount:
            xPoint, yPoint = self.pickRandomPoint()
            diameter = self.roomSizes[random.randrange(len(self.roomSizes))]
            killSwitch = 10
            while not self.checkForRoom((xPoint, yPoint),diameter) and killSwitch > 0:
                diameter = self.roomSizes[random.randrange(len(self.roomSizes))]
                xPoint, yPoint = self.pickRandomPoint()
                killSwitch -= 1
            if killSwitch > 0:
                self.world.get(yPoint).modify(xPoint, RoomTile(roomCount, xyPoz=(xPoint,yPoint)))
                self.world.get(yPoint).get(xPoint).setCenter(True,diameter=diameter)
                self.roomOrigins.append((xPoint, yPoint))
                self.createRoom((xPoint, yPoint),roomCount,diameter)
            roomCount += 1


    def createRoom(self, xyPoz, roomId, diameter):
        radius = diameter / 2 - 0.5
        r_squared = (radius + 0.25) ** 2 + 1
        r_min = (radius - 1) ** 2 + 1

        xOffset = int(xyPoz[0] - radius)
        yOffset = int(xyPoz[1] - radius)

        parentTile = self.world.get(xyPoz[1]).get(xyPoz[0])

        for i in range(diameter):
            y = (i - radius) ** 2
            insideTiles = False
            for j in range(diameter):
                x = (j - radius) ** 2
                outsideTilesTest = (r_min <= (x + y))
                worldRangeTest = (xOffset > 0 and xOffset < self.xSize - 1) and (yOffset > 0 and yOffset < self.ySize - 1)

                if (outsideTilesTest or insideTiles) and worldRangeTest:
                    if  self.world.get(yOffset).get(xOffset).getTileId() > 0 and ((x + y) <= r_squared):
                        child = RoomTile(
                            roomId=roomId,
                            diameter=diameter,
                            xyPoz=(xOffset, yOffset),
                            onEdge=True
                        )
                        if insideTiles and not outsideTilesTest:
                            child.setOnEdge(False)
                        self.world.get(yOffset).modify(xOffset, child)
                        # self.world[yOffset][xOffset] = child
                        child.setParentTile(parentTile)
                        parentTile.addChildren(child)
                    insideTiles = True
                elif not worldRangeTest:
                    insideTiles = True

                xOffset += 1
            xOffset = int(xyPoz[0] - radius)
            yOffset += 1

    def checkForRoom(self, xyPoz,diameter):
        radius = int((diameter-1)/2)

        xOffset = xyPoz[0] - radius
        yOffset = xyPoz[1] - radius

        canCreate = True

        for i in range(diameter):
            for j in range(diameter):
                if (xOffset > 0 and xOffset < self.xSize - 1) and \
                    (yOffset > 0 and yOffset < self.ySize - 1) and \
                    self.world.get(yOffset).get(xOffset).getTileId() < 0:
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
                if (x, y) in connectionLines and self.world.get(y).get(x).getTileId() == 2:
                    self.world.get(y).modify(x, RoadTile(xyPoz=(x,y)))

    def createPlayer(self):
        # while True:
        randomRoom = random.choice(self.roomOrigins)
        room = self.world.get(randomRoom[1]).get(randomRoom[0])
            # if not room.isBossRoom():
            #     break

        self.player = PlayerTile(xyPoz=randomRoom)
        self.player.setStandingTile(room)
        self.world.get(randomRoom[1]).modify(randomRoom[0], self.player)

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

class ThreadSafeWorld(ThreadSafeList):
    def __init__(self, xSize, ySize):
        super(ThreadSafeWorld, self).__init__()
        self.xSize = xSize
        self.ySize = ySize
        self.day = False

        for y in range(ySize):
            row = ThreadSafeList()
            for x in range(xSize):
                if y == 0 or y == ySize - 1 or x == 0 or x == xSize - 1:
                    row.push(WallTile(hitPoints=-1, xyPoz=(x, 0)))
                else:
                    row.push(WallTile(xyPoz=(x, y)))
            self.push(row)

    def isDay(self):
        return self.day

    def dayTime(self):
        self.day = True
        for line in self.get(0, self.ySize):
            for tile in line.get(0, self.xSize):
                tile.dayTime()

    def nightTime(self):
        self.day = False
        for line in self.get(0,self.ySize):
            for tile in line.get(0,self.xSize):
                tile.nightTime()
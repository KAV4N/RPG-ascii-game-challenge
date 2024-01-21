from colors.colorPalettes import FgColor
from tiles.tile import Tile

class PlayerTile(Tile):
    def __init__(self,xyPoz=(0,0)):
        super(PlayerTile, self).__init__(xyPoz=xyPoz)
        self.id = 0
        self.fgColor = FgColor.lightgreen
        self.tile = "#"
        self.standingTile = None

    def setStandingTile(self,tile):
        self.standingTile = tile

    def moveUp(self, worldMap):
        if worldMap[self.xyPoz[1] - 1][self.xyPoz[0]].getTileId() < 0:
            worldMap[self.xyPoz[1]][self.xyPoz[0]] = self.standingTile
            self.xyPoz = (self.xyPoz[0],) + (self.xyPoz[1] - 1,)

            self.exchangeTiles(worldMap)


    def moveDown(self, worldMap):
        if worldMap[self.xyPoz[1] + 1][self.xyPoz[0]].getTileId() < 0:
            worldMap[self.xyPoz[1]][self.xyPoz[0]] = self.standingTile
            self.xyPoz = (self.xyPoz[0],) + (self.xyPoz[1] + 1,)

            self.exchangeTiles(worldMap)


    def moveLeft(self, worldMap):
        if worldMap[self.xyPoz[1]][self.xyPoz[0]-1].getTileId() < 0:
            worldMap[self.xyPoz[1]][self.xyPoz[0]] = self.standingTile
            self.xyPoz = (self.xyPoz[0] - 1,) + (self.xyPoz[1],)

            self.exchangeTiles(worldMap)


    def moveRight(self, worldMap):
        if worldMap[self.xyPoz[1]][self.xyPoz[0] + 1].getTileId() < 0:
            worldMap[self.xyPoz[1]][self.xyPoz[0]] = self.standingTile
            self.xyPoz = (self.xyPoz[0] + 1,) + (self.xyPoz[1],)

            self.exchangeTiles(worldMap)

    def exchangeTiles(self, worldMap):
        self.standingTile = worldMap[self.xyPoz[1]][self.xyPoz[0]]
        worldMap[self.xyPoz[1]][self.xyPoz[0]] = self




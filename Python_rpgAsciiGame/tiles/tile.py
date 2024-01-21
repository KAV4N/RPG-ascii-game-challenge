from colors.colorPalettes import FgColor

class Tile:
    def __init__(self,hitPoints = 1,xyPoz = (0,0)):
        self.hitPoints = hitPoints
        self.id = 0
        self.fgColor = FgColor.lightcyan
        self.tile = ""
        self.xyPoz = xyPoz

    def decrementHitPoints(self, val=1):
        destroyed = False
        if self.hitPoints > 0:
            self.hitPoints -= val
            if self.hitPoints <= 0:
                self.hitPoints = 0
                destroyed = True
        else:
            destroyed = True
        return destroyed

    def setHitPoints(self, hitPoints):
        self.hitPoints = hitPoints

    def getHitPoints(self):
        return self.hitPoints

    def setTilePoz(self, x, y):
        self.xyPoz = (x, y)

    def getTileData(self):
        return (self.xyPoz, self.fgColor, self.tile)

    def getTileChar(self):
        return self.tile

    def getTilePoz(self):
        return self.xyPoz

    def getTileId(self):
        return self.id

    def getTileFgColor(self):
        return self.fgColor
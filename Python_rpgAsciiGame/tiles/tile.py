from colors.colorPalettes import FgColor

class Tile:
    def __init__(self,hitPoints = 1,xyPoz = (0,0)):
        self.hitPoints = hitPoints
        self.id = 0
        self.mainColor = FgColor.lightcyan
        self.fgColor = FgColor.black
        self.tile = ""
        self.xyPoz = xyPoz
        self.stepped = False
        self.lineOfSight = False
        self.trapsEnabled = False

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

    def action(self,*args,**kwargs):
        return None

    def isStepped(self):
        return self.stepped

    def setStepped(self, stepped):
        self.stepped = stepped

    def setLineOfSight(self,los):
        self.lineOfSight = los
        if self.lineOfSight:
            self.fgColor = self.mainColor
        else:
            self.fgColor = FgColor.black

    def nightTime(self):
        self.trapsEnabled = True

    def dayTime(self):
        self.trapsEnabled = False


    def getLineOfSight(self):
        return self.lineOfSight
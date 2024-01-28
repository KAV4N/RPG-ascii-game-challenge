from colors.colorPalettes import FgColor
from tiles.playerTile import PlayerTile

class EnemyTile(PlayerTile):
    def __init__(self,xyPoz=(0,0)):
        super(EnemyTile, self).__init__(xyPoz=xyPoz)
        self.id = 1
        self.mainColor = FgColor.orange
        self.fgColor = FgColor.orange
        self.tile = "#"
        self.standingTile = None
        self.weapon = None

    def exchangeTiles(self, worldMap):
        self.standingTile = worldMap.get(self.xyPoz[1]).get(self.xyPoz[0])
        self.standingTile.setStepped(True)
        worldMap.get(self.xyPoz[1]).modify(self.xyPoz[0], self)

    def moveTo(self,worldMap,x,y):
        self.standingTile.setStepped(False)
        worldMap.get(self.xyPoz[1]).modify(self.xyPoz[0], self.standingTile)
        self.xyPoz = (x,y)
        self.exchangeTiles(worldMap)





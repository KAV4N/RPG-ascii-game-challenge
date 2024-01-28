from colors.colorPalettes import FgColor
from tiles.tile import Tile




class PlayerTile(Tile):
    def __init__(self,xyPoz=(0,0)):
        super(PlayerTile, self).__init__(xyPoz=xyPoz)
        self.id = 0
        self.fgColor = FgColor.lightgreen
        self.tile = "#"
        self.standingTile = None
        self.weapon = None

    def setStandingTile(self,tile):
        self.standingTile = tile
        self.standingTile.setStepped(True)



    def moveUp(self, worldMap,terminal):
        if worldMap.get(self.xyPoz[1] - 1).get(self.xyPoz[0]).getTileId() < 0:
            self.standingTile.setStepped(False)
            worldMap.get(self.xyPoz[1]).modify(self.xyPoz[0], self.standingTile)
            self.xyPoz = (self.xyPoz[0],) + (self.xyPoz[1] - 1,)
            self.exchangeTiles(worldMap,terminal)




    def moveDown(self, worldMap,terminal):
        if worldMap.get(self.xyPoz[1] + 1).get(self.xyPoz[0]).getTileId() < 0:
            self.standingTile.setStepped(False)
            worldMap.get(self.xyPoz[1]).modify(self.xyPoz[0], self.standingTile)
            self.xyPoz = (self.xyPoz[0],) + (self.xyPoz[1] + 1,)
            self.exchangeTiles(worldMap,terminal)


    def moveLeft(self, worldMap,terminal):
        if worldMap.get(self.xyPoz[1]).get(self.xyPoz[0] - 1).getTileId() < 0:
            self.standingTile.setStepped(False)
            worldMap.get(self.xyPoz[1]).modify(self.xyPoz[0], self.standingTile)
            self.xyPoz = (self.xyPoz[0] - 1,) + (self.xyPoz[1],)
            self.exchangeTiles(worldMap,terminal)



    def moveRight(self, worldMap,terminal):
        if worldMap.get(self.xyPoz[1]).get(self.xyPoz[0] + 1).getTileId() < 0:
            self.standingTile.setStepped(False)
            worldMap.get(self.xyPoz[1]).modify(self.xyPoz[0], self.standingTile)
            self.xyPoz = (self.xyPoz[0] + 1,) + (self.xyPoz[1],)
            self.exchangeTiles(worldMap,terminal)


    def exchangeTiles(self, worldMap,terminal):
        self.standingTile = worldMap.get(self.xyPoz[1]).get(self.xyPoz[0])
        self.getWeapon(worldMap,terminal)

        ######### ONLY FOR TEST PURPOSES!!! ########
        if self.weapon:
            terminal.testData = self.weapon.getName()
        else:
            terminal.testData = self.weapon
        ############################################


        self.standingTile.setStepped(True)
        worldMap.get(self.xyPoz[1]).modify(self.xyPoz[0], self)

    def getWeapon(self,worldMap, terminal):
        weapon = self.standingTile.action(worldMap,terminal,self.weapon)
        if not self.weapon:
            self.weapon = weapon
        elif self.weapon.isUsed():
            self.weapon = weapon

    def attack(self):
        if self.weapon:
            if self.weapon.use() or self.weapon.isUsed():
                self.weapon = None



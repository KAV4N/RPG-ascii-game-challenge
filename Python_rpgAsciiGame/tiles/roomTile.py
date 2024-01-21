from colors.colorPalettes import FgColor
from tiles.tile import Tile

class RoomTile(Tile):
    def __init__(self,roomId = 1,diameter=1,xyPoz = (0,0)):
        super(RoomTile, self).__init__(xyPoz=xyPoz)
        self.roomId = roomId
        self.diameter = diameter
        self.id = -1
        self.fgColor = FgColor.lightgrey
        self.tile = "."
        self.center = False

    def setCenter(self,center):
        self.center = center
        if self.center:
            self.tile = "R"

    def getCenter(self):
        return self.center

    def getRoomId(self):
        return self.roomId

    def setRoomId(self,roomId):
        self.roomId = roomId

    def setDiameter(self,diameter):
        self.diameter = diameter
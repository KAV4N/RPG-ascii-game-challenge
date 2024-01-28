from colors.colorPalettes import FgColor
from tiles.tile import Tile

class RoadTile(Tile):
    def __init__(self,xyPoz = (0,0)):
        super(RoadTile, self).__init__(xyPoz=xyPoz)
        self.id = -1
        # self.fgColor = FgColor.lightgrey
        self.mainColor = FgColor.lightgrey
        self.tile = "-"

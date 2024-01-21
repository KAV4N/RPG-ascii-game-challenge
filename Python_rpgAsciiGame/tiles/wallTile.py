from colors.colorPalettes import FgColor
from colors.colorPalettes import BgColor
from tiles.tile import Tile

class WallTile(Tile):
    def __init__(self,hitPoints=1,xyPoz = (0,0)):
        super(WallTile, self).__init__(hitPoints=hitPoints,xyPoz=xyPoz)
        self.id = 1
        self.tile = "@"
        self.fgColor = FgColor.cyan
        if self.hitPoints == -1:
            self.fgColor = FgColor.red




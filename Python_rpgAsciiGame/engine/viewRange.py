import math

class ViewRange:
    def __init__(self, worldMap, player):
        self.worldMap = worldMap
        self.xSize = self.worldMap.get(0).length()
        self.ySize = self.worldMap.length()
        self.lineOfSightTiles = set()
        self.viewRange = 7
        self.player = player

    def setViewRange(self, vRange):
        self.viewRange = vRange

    def bresenhamLine(self, x1, y1, x2, y2):
        """Bresenham's Line Algorithm."""
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return points

    def updateLineOfSight(self):
        x, y = self.player.getTilePoz()
        visibleTiles = set()


        range_x = range(max(0, x - self.viewRange), min(self.xSize, x + self.viewRange + 1))
        range_y = range(max(0, y - self.viewRange), min(self.ySize, y + self.viewRange + 1))

        for i in range_y:
            for j in range_x:
                distance = math.sqrt((x - j) ** 2 + (y - i) ** 2)
                if distance <= self.viewRange:
                    lineOfSight = self.bresenhamLine(x, y, j, i)
                    for point in lineOfSight:
                        # if 0 <= point[0] < ySize and 0 <= point[1] < xSize:
                        tile = self.worldMap.get(point[1]).get(point[0])
                        if tile.getTileId() < 0:
                            tile.setLineOfSight(True)
                            visibleTiles.add(tile)
                        elif tile.getTileId() > 0:
                            break

        self.clearLineOfSight(newTiles=visibleTiles)


    def clearLineOfSight(self, newTiles=set()):
        resultTiles = self.lineOfSightTiles.difference(newTiles)
        for tile in resultTiles:
            tile.setLineOfSight(False)
        self.lineOfSightTiles = newTiles.copy()

    def getViewRangeItems(self):
        return self.lineOfSightTiles
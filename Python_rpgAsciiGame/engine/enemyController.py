import threading
import time
import math

from engine.viewRange import ViewRange
from engine.viewRange import ViewRange
from tiles.tile import Tile


class EnemyController(threading.Thread):
    def __init__(self, enemy, terminal):
        super(EnemyController, self).__init__()
        self.enemy = enemy
        self.terminal = terminal
        self.viewRange = EnemyViewRange(self.terminal.getWorldMap(), enemy)
        self.worldMap = self.terminal.getWorldMap()

    def run(self):
        time.sleep(2)
        camCompenzation = 10
        while self.terminal.isOpen:
            xStartPoz, yStartPoz, xEndPoz, yEndPoz = self.terminal.camera.getCurPozition()
            curPoz = self.enemy.getTilePoz()
            if (curPoz[0] > (xStartPoz-camCompenzation) and curPoz[0] < (xEndPoz+camCompenzation)) and (curPoz[1] > (yStartPoz-camCompenzation) and curPoz[1] < (yEndPoz+camCompenzation)):
                xyPlayerPoz , xyViewRangePoz = self.viewRange.updateLineOfSight()
                if xyPlayerPoz:
                    self.moveTowardsPlayer(xyPlayerPoz,xyViewRangePoz)
                elif xyViewRangePoz:
                    self.moveTowardsClosestTiles(xyViewRangePoz)

            time.sleep(0.12)

    def moveTowardsPlayer(self, xyPlayerPoz, xyViewRangePoz):
        enemyX, enemyY = self.enemy.getTilePoz()
        playerX, playerY = xyPlayerPoz
        self.move(playerX,playerY, enemyX, enemyY,xyViewRangePoz=xyViewRangePoz)

    def moveTowardsClosestTiles(self, xyViewRangePoz, numTiles=10):
        enemyX, enemyY = self.enemy.getTilePoz()
        distances = []

        for playerPoz in xyViewRangePoz:
            distance = math.sqrt((enemyX - playerPoz[0]) ** 2 + (enemyY - playerPoz[1]) ** 2)
            distances.append((distance, playerPoz))

        distances.sort(key=lambda x: x[0])
        closestTiles = distances[:numTiles]

        for distance, closestTilePoz in closestTiles:
            self.move(closestTilePoz[0], closestTilePoz[1], enemyX, enemyY)
            xyPlayerPoz , xyViewRangePoz = self.viewRange.updateLineOfSight()
            if xyPlayerPoz:
                break

    # def moveTowardsClosestPlayer(self, xyViewRangePoz):
    #     enemyX, enemyY = self.enemy.getTilePoz()
    #
    #     minDistance = float('inf')
    #     closestPlayerPoz = None
    #
    #     for playerPoz in xyViewRangePoz:
    #         distance = math.sqrt((enemyX - playerPoz[0]) ** 2 + (enemyY - playerPoz[1]) ** 2)
    #         if distance < minDistance:
    #             minDistance = distance
    #             closestPlayerPoz = playerPoz
    #
    #     if closestPlayerPoz:
    #         self.move(closestPlayerPoz[0], closestPlayerPoz[1], enemyX, enemyY)

    def move(self, playerX, playerY, enemyX, enemyY,xyViewRangePoz=()):
        dx = 1 if playerX > enemyX else -1 if playerX < enemyX else 0
        dy = 1 if playerY > enemyY else -1 if playerY < enemyY else 0

        nextX = enemyX + dx
        nextY = enemyY + dy
        nextTileId = self.worldMap.get(nextY).get(nextX).getTileId()
        if  nextTileId < 0:
            self.enemy.moveTo(self.worldMap, nextX, nextY)
        elif nextTileId==2 and xyViewRangePoz:
            self.moveTowardsClosestTiles(xyViewRangePoz)

class EnemyViewRange(ViewRange):
    def __init__(self, worldMap, enemy):
        super(EnemyViewRange, self).__init__(worldMap, enemy)
        self.viewRange = 12

    def updateLineOfSight(self):
        x, y = self.player.getTilePoz()
        xyPlayerPoz = tuple()
        xyViewRangePoz = set()
        range_x = range(max(0, x - self.viewRange), min(self.xSize, x + self.viewRange + 1))
        range_y = range(max(0, y - self.viewRange), min(self.ySize, y + self.viewRange + 1))

        for i in range_y:
            for j in range_x:
                distance = math.sqrt((x - j) ** 2 + (y - i) ** 2)
                if distance <= self.viewRange:
                    lineOfSight = self.bresenhamLine(x, y, j, i)
                    for point in lineOfSight:
                        tile = self.worldMap.get(point[1]).get(point[0])
                        if tile.getTileId() < 1:
                            if tile.getTileId() == 0:
                                xyPlayerPoz = point
                                break
                            if tile.getLineOfSight():
                                xyViewRangePoz.add(point)
                        elif tile.getTileId() > 1:
                            break
            if xyPlayerPoz:
                break

        self.clearLineOfSight(xyViewRangePoz)
        return xyPlayerPoz, self.lineOfSightTiles

    def clearLineOfSight(self, newTiles=set()):
        resultTiles = self.lineOfSightTiles.difference(newTiles)
        self.lineOfSightTiles = newTiles.copy()
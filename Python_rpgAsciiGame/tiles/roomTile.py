import random

from colors.colorPalettes import FgColor
from tiles.tile import Tile
from tiles.enemyTile import EnemyTile
from engine.enemyController import EnemyController
from tiles.weapons.flashlight import Flashlight

import math


class RoomTile(Tile):
    def __init__(self,roomId = 1,diameter=1,xyPoz = (0,0),onEdge = False):
        super(RoomTile, self).__init__(xyPoz=xyPoz)

        self.maxCoverageArea = 5 # percentage
        self.maxEnemies = self.calculateEnemies(diameter)
        self.roomId = roomId
        self.diameter = diameter
        self.id = -1
        self.maxEnemies = 3



        self.baseColor = FgColor.lightgrey
        self.activeBorderColor = FgColor.red
        self.notActiveBorderColor = FgColor.orange
        self.weaponActiveColor = FgColor.purple

        self.bossRoom = False
        self.raided = False
        self.onEdge = onEdge

        if not self.onEdge:
            self.mainColor = self.baseColor
        else:
            self.mainColor = self.notActiveBorderColor
        if self.diameter > 9:
            self.bossRoom = True
        else:
            self.mainColor = self.baseColor
            self.onEdge = False

        self.tile = "."
        self.center = False
        self.enemyEntities = None
        self.children = None
        self.roomClosed = False
        self.parentTile = None

        self.weaponAvailable = True


    def calculateEnemies(self, diameter):
        roomRadius = (diameter-2) / 2
        roomArea = math.pi * roomRadius ** 2
        maxEnemies = int(roomArea * (self.maxCoverageArea / 100))
        if maxEnemies == 0:
            maxEnemies = 1
        elif maxEnemies > 3:
            maxEnemies = 3
        return maxEnemies

    def addChildren(self,child):
        self.children+=(child,)

    def setWeaponActive(self):
        self.mainColor = self.weaponActiveColor

    def pickUpWeapon(self,worldMap, terminal):
        weapon = None
        if self.weaponAvailable:
            weapon = Flashlight(worldMap,terminal)
            self.mainColor = self.baseColor
            self.weaponAvailable = False
        return weapon

    def setCenter(self,center,diameter=1):
        self.center = center
        if self.center:
            self.onEdge = False
            self.tile = "R"
            self.diameter = diameter
            if self.diameter > 9:
                self.bossRoom = True
                self.setWeaponActive()
            self.enemyEntities = []
            self.children = ()
            self.maxEnemies = self.calculateEnemies(diameter)


    def getCenter(self):
        return self.center

    def getRoomId(self):
        return self.roomId

    def setRoomId(self,roomId):
        self.roomId = roomId

    def setDiameter(self,diameter):
        self.diameter = diameter


    def closeTile(self):
        self.id = 2
        self.mainColor = self.activeBorderColor

    def openTile(self):
        self.id = -1
        self.mainColor = self.notActiveBorderColor

    def isOnEdge(self):
        return self.onEdge

    def setOnEdge(self,onEdge):
        if onEdge and self.bossRoom:
            self.mainColor = self.notActiveBorderColor
        else:
            self.mainColor = self.baseColor
        self.onEdge = onEdge

    def closeAllRoomTiles(self):
        if not self.roomClosed and self.center:
            self.roomClosed = True
            for child in self.children:
                if child.isOnEdge():
                    child.closeTile()

    def openAllRoomTiles(self):
        if self.roomClosed and self.center:
            self.roomClosed = False
            for child in self.children:
                if child.isOnEdge():
                    child.openTile()

    def createEnemies(self, worldMap,filterPoz = None,terminal=None):
        if self.center and len(self.enemyEntities) == 0:
            self.enemyEntities.clear()
            while len(self.enemyEntities) < self.maxEnemies:
                child = random.choice(self.children)
                poz = child.getTilePoz()
                if not child.isOnEdge() and (child not in self.enemyEntities) and (poz != filterPoz):
                    enemy = EnemyTile(poz)
                    enemy.setStandingTile(child)
                    enemyController = EnemyController(enemy,terminal=terminal)
                    enemyController.start()

                    self.enemyEntities.append(enemy)
                    worldMap.get(poz[1]).modify(poz[0], enemy)

    def moveInEnemyEntities(self,worldMap,terminal,filterPoz = None):
        if self.enemyEntities:
            placed = 0
            for enemy in self.enemyEntities:
                while placed < len(self.enemyEntities):
                    child = random.choice(self.children)
                    poz = child.getTilePoz()
                    if not child.isOnEdge() and (poz != filterPoz):
                        enemy.moveTo(worldMap,x=poz[0],y=poz[1])
                        placed+=1

    def setParentTile(self,parentTile):
        self.parentTile = parentTile

    def action(self,worldMap,terminal,playerWeapon):
        weapon = playerWeapon
        if not self.onEdge and self.bossRoom and not self.center:
            # if not self.parentTile.roomClosed:
                # if self.trapsEnabled:
                    # self.parentTile.moveInEnemyEntities(worldMap,terminal,filterPoz = self.xyPoz)
                    # self.parentTile.closeAllRoomTiles()
            self.parentTile.createEnemies(worldMap,filterPoz = self.xyPoz, terminal=terminal)
            # elif not self.trapsEnabled and self.parentTile.roomClosed:
            #     self.parentTile.openAllRoomTiles()
        elif self.center and self.bossRoom and not playerWeapon:
            weapon = self.pickUpWeapon(worldMap,terminal)
        return weapon


    def isStepped(self):
        return self.stepped

    def nightTime(self):
        self.trapsEnabled = True

    def dayTime(self):
        self.trapsEnabled = False

    def setStepped(self,stepped):
        self.stepped = stepped

    def isBossRoom(self):
        return self.bossRoom




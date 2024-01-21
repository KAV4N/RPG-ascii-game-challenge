import threading
import os
import time
import keyboard
from engine.camera import Camera
from colors.colorPalettes import Colors


class Terminal(threading.Thread):
    def __init__(self, FPS=60, world=None):
        super(Terminal, self).__init__()
        self.world = world
        self.camera = Camera(focusOn=self.world.getPlayer())
        self.worldMap = self.world.getWorld()
        self.FPS = 1000/FPS
        self.isOpen = False

    def run(self):
        self.isOpen = True
        if self.world:
            while self.isOpen:
                self.refresh()
                if keyboard.is_pressed("f"):
                    self.closeTerminal()
                time.sleep(self.FPS/1000)


    def refresh(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.showFrame()

    def showFrame(self):
        xStartPoz, yStartPoz, xEndPoz, yEndPoz = self.camera.moveCamera(self.world.getXSize(), self.world.getYSize())
        for line in self.worldMap[yStartPoz:yEndPoz]:
            for tile in line[xStartPoz:xEndPoz]:
                print(tile.getTileFgColor(), tile.getTileChar(), end="")
            print(Colors.reset)

    def move_cursor(self, x,y):
        print(f"\033[{y};{x}H", end="")

    def addToBuffer(self,data=[]):
        self.buffer.append(data)

    def setFPS(self,FPS):
        self.FPS = 1000/FPS

    def closeTerminal(self):
        self.isOpen = False

    def getWorldMap(self):
        return self.worldMap
import threading
import time
import math
import keyboard
from engine.viewRange import ViewRange

class PlayerController(threading.Thread):
    def __init__(self, player, terminal):
        super(PlayerController, self).__init__()
        self.player = player
        self.terminal = terminal
        self.viewRange = ViewRange(self.terminal.getWorldMap(), player)

    def updateLineOfSight(self):
        self.viewRange.updateLineOfSight()

    def run(self):
        while self.terminal.isOpen:
            if keyboard.is_pressed('left'):
                self.player.moveLeft(self.terminal.getWorldMap(),self.terminal)

            if keyboard.is_pressed('right'):
                self.player.moveRight(self.terminal.getWorldMap(),self.terminal)


            if keyboard.is_pressed('up'):
                self.player.moveUp(self.terminal.getWorldMap(),self.terminal)


            if keyboard.is_pressed('down'):
                self.player.moveDown(self.terminal.getWorldMap(),self.terminal)


            if keyboard.is_pressed('f') or keyboard.is_pressed('F'):
                self.player.attack()

            self.updateLineOfSight()
            time.sleep(0.1)




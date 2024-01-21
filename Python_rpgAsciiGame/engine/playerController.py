import threading
import time

import keyboard

class PlayerController(threading.Thread):
    def __init__(self, player, terminal):
        super(PlayerController, self).__init__()
        self.player = player
        self.terminal = terminal

    def run(self):
        while self.terminal.isOpen:
            if keyboard.is_pressed('left'):
                self.player.moveLeft(self.terminal.getWorldMap())
            if keyboard.is_pressed('right'):
                self.player.moveRight(self.terminal.getWorldMap())
            if keyboard.is_pressed('up'):
                self.player.moveUp(self.terminal.getWorldMap())
            if keyboard.is_pressed('down'):
                self.player.moveDown(self.terminal.getWorldMap())
            time.sleep(0.1)


import threading
import time


class Weapon(threading.Thread):
    def __init__(self, worldMap, terminal):
        super(Weapon, self).__init__()
        self.worldMap = worldMap
        self.terminal = terminal
        self.used = False
        self.name = "Weapon"

    def use(self):
        self.start()

    def isUsed(self):
        return self.used

    def run(self):
        self.used = True

    def getName(self):
        return self.name

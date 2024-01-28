import time
from tiles.weapons.weapon import Weapon

class Flashlight(Weapon):
    def __init__(self,worldMap,terminal):
        super(Flashlight, self).__init__(worldMap,terminal)
        self.dTime = 5 #seconds
        self.name = "Flashlight"

    def use(self):
        success = False
        if not self.worldMap.isDay():
            self.start()
            success = True
        return success

    def run(self):
        self.dayTime()
        self.nightTime()
        self.used = True

    def dayTime(self):
        self.worldMap.dayTime()
        for i in range(self.dTime):
            if self.terminal.isOpen:
                time.sleep(1)
            else:
                break

    def nightTime(self):
        self.worldMap.nightTime()


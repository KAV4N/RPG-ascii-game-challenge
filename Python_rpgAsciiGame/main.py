
from engine.terminal import Terminal
from engine.worldGenerator import WorldGenerator
from engine.playerController import PlayerController

class Application:
    def __init__(self):
        self.FPS = 60
        self.xWorldSize = 100
        self.yWorldSize = 100
        self.rooms = 20

        self.world = WorldGenerator(x=self.xWorldSize, y=self.yWorldSize, rooms=self.rooms)
        self.terminal = Terminal(self.FPS,self.world)
        self.playerController = PlayerController(player=self.world.getPlayer(), terminal=self.terminal)

    def play(self):
        self.terminal.start()
        self.playerController.start()



if __name__ == "__main__":
    app = Application()
    app.play()
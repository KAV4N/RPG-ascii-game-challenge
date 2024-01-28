from tiles.weapons.weapon import Weapon

class Spell(Weapon):
    def __init__(self):
        super(Spell, self).__init__(worldMap,terminal)
        self.range = 1
        self.dmg = 1
        self.cooldown = 2 #seconds

    def use(self):
        pass

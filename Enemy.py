import random
class enemy:
    def __init__(self):
        self.maxhp=10
        self.speed=3
        self.dmg=1
        self.gamemode=random.choice(["bot1","wall"])
        self.height=100

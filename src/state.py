from game import *
from aux import InfoSheetLoader

class STATECONST:
    
    STATE_IDLE = 0
    STATE_WALK = 1
    STATE_BLCK = 2
    STATE_HIT  = 3
    STATE_ATK = 4
    STATE_WIN = 5



class PlayerState():
    
    def __init__(self, filename, facingRight, position = Point(0,0)):
        self.position = position

        filename = '../res/Char/' + filename + '/' + filename
        self.charInfo = InfoSheetLoader(filename + 'Move.txt').getcharInfo()
        self.maxHealth = self.charInfo.health
        self.health = self.charInfo.health

        self.facingRight = facingRight
        self.state = STATECONST.STATE_IDLE

    def get_position(self):
        return self.position

    def lose_hp(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def am_i_dead(self):
        return self.health == 0

    def set_state(self, state):
        self.state = state

    def getState(self, curent_anim):
        # return self.state

        switch = curent_anim
        if switch == 0:
            return STATECONST.STATE_IDLE
        elif switch == 1:
            return STATECONST.STATE_WALK
        elif switch == 8:
            return STATECONST.STATE_BLCK
        elif 9 <= switch <= 10:
            return STATECONST.STATE_HIT
        elif switch == 17:
            return STATECONST.STATE_WIN 
        else:
            return STATECONST.STATE_ATK    

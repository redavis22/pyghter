from utils import *
from random import randint

class STATES:    
    STATE_IDLE = 0
    STATE_FORW = 1
    STATE_BACK = 2
    
    STATE_JUMP_1 = 3
    STATE_JUMP_2 = 4
    STATE_JUMP_3 = 5
    STATE_JUMP_LIGHT_ATK = 6

    STATE_LIGHT_ATK = 7
    STATE_HARD_ATK = 8

    STATE_INJURE = 9
    STATE_BLOCK = 10

    STATE_FALL_1 = 11
    STATE_FALL_2 = 12
    STATE_FALL_3 = 13

class ACTIONS:
    NONE = 0
    FORWARD = 1
    BACK = 2
    JUMP = 3
    JUMP_FORW = 4
    JUMP_BACK = 5
    LIGHT_ATK = 6

class Action:
    
    def __init__(self, maxts=0):
        self.ts = 0
        self.maxts = maxts

    def combine(self, action):
        if isinstance(action, FallAction):
            return action
        if isinstance(action, InjureAction):
            return action

        if self._done():
            return action
        else:
            return self

    def _done(self):
        return self.ts > self.maxts

    def attack(self):
        return False

    def apply(self, state):
        self.ts += 1
        return self._apply(state)


class IdleAction(Action):

    def _apply(self, state):
        state.state = STATES.STATE_IDLE


class WalkForwAction(Action):

    def _apply(self, state):
        sign = 1 if state.facing_right else -1
        state.position += Vector(sign * 8, 0)
        state.state = STATES.STATE_FORW


class WalkBackAction(Action):

    def _apply(self, state):
        sign = 1 if state.facing_right else -1
        state.position -= Vector(sign * 4, 0)
        state.state = STATES.STATE_BACK


class BlockAction(Action):

    def __init__(self):
        Action.__init__(self, 3)

    def _apply(self, state):
        state.state = STATES.STATE_BLOCK


class JumpAction(Action):
    
    def __init__(self, dx=0):
        Action.__init__(self, 7)
        self.ts = 0
        # last up ts
        self.ts_up = 4
        self.dx = dx
        self.dy = 20

        self.hit_width = 23
        self.hit_height = 12
        self.hit = False
        self.damage = 0

        self.attack_ts = -1

    def _apply(self, state):
        p = state.position
        sign = 1 if state.facing_right else -1

        s = None
        
        if self.ts == 0:
            s = STATES.STATE_JUMP_1
        elif self.ts >= 1 and self.ts <= self.ts_up:
            s = STATES.STATE_JUMP_2
            p = p + Vector(sign * self.dx, -self.dy)
        elif self.ts > self.ts_up:
            s = STATES.STATE_JUMP_3
            p = p + Vector(sign * self.dx, self.dy)
        
        if self.attack():
            s = STATES.STATE_JUMP_LIGHT_ATK
            self.damage = 10
        else:
            self.damage = 0
        
        state.state = s
        state.position = p

    def combine(self, action):
        # print(action.__class__.__name__)
        if isinstance(action, FallAction):
            return FallJumpAction()
        if isinstance(action, InjureAction):
            return FallJumpAction()
        elif isinstance(action, LightAttackAction):
            self.attack_ts = self.ts
        
        if self._done():
            return action
        else:
            return self

    def attack(self):
        return not self.hit and self.attack_ts > 0 and self.ts - self.attack_ts < 2 

    def hit_rect(self, state):
        sign = 1 if state.facing_right else -1
        x = state.position.x

        if state.facing_right:
            x += int(state.width / 2)
        else:
            x -= int(state.width / 2) + int(self.hit_width / 3) * self.ts
        
        position = Point(x, state.position.y - int(state.height * 3 / 7) - self.hit_height)

        return Rect(int(self.hit_width / 3) * self.ts, self.hit_height, position)        


class InjureAction(Action):
    
    def __init__(self):
        Action.__init__(self, 3)

    def _apply(self, state):
        state.state = STATES.STATE_INJURE


class FallAction(Action):
    
    def __init__(self):
        Action.__init__(self, 8)

    def _apply(self, state):
        if self.ts < 4:
            sign = 1 if state.facing_right else -1
            state.position -= Vector(sign * 5, 0)
            state.state = STATES.STATE_FALL_1
        elif self.ts == 4:
            state.state = STATES.STATE_FALL_2
        else:
            state.state = STATES.STATE_FALL_3

class FallJumpAction(Action):
    
    MIN_Y = 195

    def __init__(self):
        Action.__init__(self, 5)
    
    def apply(self, state):
        print(self.ts)
        if self.ts == 0:
            sign = 1 if state.facing_right else -1
            state.position -= Vector(sign * 10, -15)
            state.state = STATES.STATE_FALL_1
            if state.position.y >= FallJumpAction.MIN_Y:
                state.position.y = FallJumpAction.MIN_Y
                self.ts += 1
        elif self.ts == 1:
            state.state = STATES.STATE_FALL_2
            self.ts += 1
        elif self.ts >= 2:
            state.state = STATES.STATE_FALL_3
            self.ts += 1

    
class LightAttackAction(Action):

    def __init__(self):
        Action.__init__(self, 3)
        self.hit_width = 23
        self.hit_height = 12
        self.hit = False
        self.damage = 10

    def _apply(self, state):
        state.state = STATES.STATE_LIGHT_ATK

    def hit_rect(self, state):
        sign = 1 if state.facing_right else -1
        x = state.position.x

        if state.facing_right:
            x += int(state.width / 2)
        else:
            x -= int(state.width / 2) + int(self.hit_width / 3) * self.ts
        
        position = Point(x, state.position.y - int(state.height * 3 / 7) - self.hit_height)

        return Rect(int(self.hit_width / 3) * self.ts, self.hit_height, position)        

    def attack(self):
        return not self.hit and not self._done()


class HardAttackAction(Action):

    def __init__(self):
        Action.__init__(self, 7)
        self.ts = 0
        self.hit = False
        self.hit_width = 42
        self.hit_height = 12
        self.damage = 15

    def _apply(self, state):
        sign = 1 if state.facing_right else -1
        state.position += Vector(sign * 4, 0)
        state.state = STATES.STATE_HARD_ATK

    def attack(self):
        return False

    def hit_rect(self, state):
        sign = 1 if state.facing_right else -1
        x = state.position.x

        if state.facing_right:
            x += int(state.width / 2)
        else:
            x -= int(state.width / 2) + int(self.hit_width / 3)
        
        position = Point(x, state.position.y - int(state.height * 3 / 7) - self.hit_height)

        return Rect(int(self.hit_width / 3), self.hit_height, position)        

    def attack(self):
        return not self.hit and not self._done()



class WarriorState():
    
    def __init__(self, facing_right, position):
        self.position = position
        self.facing_right = facing_right
        self.state = STATES.STATE_IDLE
        self.health = 142
        self.maxHealth = 142
        self.width = 16
        self.height = 38

    def set_state(self, state):
        self.state = state

    def getStateNum(self):
        return self.state

    def get_rect(self):
        return Rect(self.width, self.height, Point(self.position.x - int(self.width / 2) , 
            self.position.y - self.height))
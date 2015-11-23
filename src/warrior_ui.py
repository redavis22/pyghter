from random import randint
from warrior import *

class WarriorUi:

    def __init__(self, state, screen, sprite_file):
        self.sprite_width = 120
        self.sprite_height = 100

        self.health = HealthBar(state, state.facing_right)

        self.sprite_list = SpriteSheetLoader(sprite_file, self.sprite_width, self.sprite_height).getSpriteList()
        self.screen = screen

        self.state = state
        self.prev_s = state.state
        self.cur_anim = self.get_curent_anim()
        self.frame = 0


    def print_me(self):

        print_point = self.state.position - (int(self.sprite_width / 2), self.sprite_height)

        if self.prev_s != self.state.state:
            self.frame = 0
            self.prev_s = self.state.state
            self.cur_anim = self.get_curent_anim()
        
        sprite_line = self.sprite_list[self.cur_anim]
        sprite = sprite_line[self.frame]
        if not self.state.facing_right:
            sprite = pygame.transform.flip(sprite, 1, 0)
        
        self.screen.blit(sprite, print_point.value())

        self.frame += 1
        if self.frame >= len(sprite_line):
            self.frame = 0


        self.health.print_me(self.screen)

    def get_curent_anim(self):
        s = self.state.state
        if s == STATES.STATE_IDLE:
            return 0
        elif s == STATES.STATE_FORW or s == STATES.STATE_BACK:
            return 1
        elif s == STATES.STATE_JUMP_1:
            return 5
        elif s == STATES.STATE_JUMP_2:
            return 6
        elif s == STATES.STATE_JUMP_3:
            return 7
        elif s == STATES.STATE_JUMP_LIGHT_ATK:
            return 25 + randint(0, 2)
        elif s == STATES.STATE_LIGHT_ATK:
            return 21 + randint(0, 2)
        elif s == STATES.STATE_HARD_ATK:
            return 24
        elif s == STATES.STATE_INJURE:
            return 9 + randint(0,1)
        elif s == STATES.STATE_BLOCK:
            return 8
        elif s == STATES.STATE_FALL_1:
            return 12
        elif s == STATES.STATE_FALL_2:
            return 14
        elif s == STATES.STATE_FALL_3:
            return 15

class HealthBar:
    def __init__(self, player_state, orientation = True):
        self.player_state = player_state

        if orientation:
            self.position = Point(8, 8)
        else:
            self.position = Point(170, 8)
        
        self.orientation = orientation
        self.hp = 142
        self.trail = 142
        self.tick = 0
    
    def reinit(self):
        self.hp = 142
        self.trail = 142
    
    def tick_me(self, int):
        if self.tick < int:
            self.tick += 1
            return
        if self.trail > self.hp:
            self.trail -= 1
        self.tick = 0
    
    def print_me(self, screen):
        self.hp = int((self.player_state.health/self.player_state.maxHealth) * 142)
        if self.hp > 0:
            surface = pygame.Surface((self.trail, 7)).convert()
            surface.fill((255,90,30))
            if self.orientation:
                screen.blit(surface, (self.position+(142-self.trail, 0)).value())
            else : screen.blit(surface, self.position.value())
            surface = pygame.Surface((self.hp, 7)).convert()
            surface.fill((255,240,30))
            if self.orientation:
                screen.blit(surface, (self.position+(142-self.hp, 0)).value())
            else : screen.blit(surface, self.position.value())

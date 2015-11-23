import pygame
import config

from utils import *
from warrior import STATES, WarriorState, IdleAction, LightAttackAction, HardAttackAction, InjureAction, FallAction 
from warrior_agent import WarriorInputAgent
from warrior_ui import WarriorUi

screen = pygame.Surface((320, 240), 0, 32)

class Background:
    def __init__(self, file):
        self.sprite = pygame.image.load(file).convert()
        self.position = Point(-160, 0)
        
    def shift_position(self, x):
        shift = 160 - x
        self.position += (shift, 0)
        
        if self.position.x > 0:
            shift = self.position.x + shift
            self.position = Point(0, 0)
        elif self.position.x < -320:
            shift = self.position.x + shift + 320
            self.position = Point(-320, 0)
            
        return Point(shift, 0)
        
    def print_me(self, screen):
        screen.blit(self.sprite, self.position.value())


class GameController:

    def __init__(self, screen, background, warrior1, warrior_ui1, warrior2, warrior_ui2):
        self.screen = screen
        self.config = config.OptionConfig()
        self.clock = pygame.time.Clock()
        self.color = (0,0,0,0)
        self.input_reader = InputReader(self.config.keysP1, self.config.keysP2)

        self.background = background
        self.background.position = Point(-160, 0)

        self.warrior1 = warrior1
        self.warrior2 = warrior2
        self.warrior_ui1 = warrior_ui1
        self.warrior_ui2 = warrior_ui2

        self.prev_action1 = IdleAction()
        self.prev_action2 = IdleAction()


    def turn_around(self, state1, state2):
        if state2.position.y != 195 or state1.position.y != 195:
            return

        if state1.facing_right and state2.position.x < state1.position.x:
            state1.facing_right = False
            state2.facing_right = True
        elif not state1.facing_right and state2.position.x > state1.position.x:
            state1.facing_right = True
            state2.facing_right = False

    def check_boundaries(self, state1, state2):
        pass

    def attack(self, action1, state1, action2, state2):
        a2 = action2
        if (action1.attack()):
            hit_rect = action1.hit_rect(state1)
            warrior_rect = state2.get_rect()

            if hit_rect.collide(warrior_rect):
                action1.hit = True
                if state2.state != STATES.STATE_BLOCK:
                    state2.health -= action1.damage
                    if action1.damage <= 10:
                        a2 = a2.combine(InjureAction())
                    else:
                        a2 = a2.combine(FallAction())

        return a2

    def apply_action(self, action1, state1, action2, state2):
        action1 = self.prev_action1.combine(action1)
        action2 = self.prev_action2.combine(action2)

        self.debug(state1, action1)
        self.debug(state2, action2)

        action1.apply(state1)
        action2.apply(state2)

        a2 = self.attack(action1, state1, action2, state2)
        a1 = self.attack(action2, state2, action1, state1)

        self.prev_action1 = a1
        self.prev_action2 = a2

        self.check_boundaries(state1, state2)
        self.turn_around(state1, state2)


    def mainloop(self):
        done = False
        while not done:
            stick_inputs_p1, btn_inputs_P1, stick_inputs_p2, btn_inputs_P2, special = self.input_reader.getInputs()
            
            if special == 'QUIT':
                return 'QUIT'

            self.screen.fill((0,0,0))
            self.background.print_me(self.screen)
            
            self.warrior1.set_inputs(stick_inputs_p1, btn_inputs_P1)
            self.warrior2.set_inputs(stick_inputs_p2, btn_inputs_P2)

            self.warrior_ui1.print_me()
            self.warrior_ui2.print_me()
            
            action1 = self.warrior1.next_action(self.warrior2.state)
            action2 = self.warrior2.next_action(self.warrior1.state)

            self.apply_action(action1, warrior1.state, action2, warrior2.state)

            config.Screen().display_update(self.screen)
            
            if warrior1.state.health <= 0 or warrior2.state.health <= 0:
                done = True
            self.clock.tick(12)

        for i in range(10):
            self.clock.tick(12)


    def debug(self, state1, action1):
        if isinstance(action1, LightAttackAction) or isinstance(action1, HardAttackAction):
            rect = action1.hit_rect(state1)
            pygame.draw.rect(screen, (0,0,255), rect.value(), 1)
        rect = state1.get_rect()
        pygame.draw.rect(screen, (0,255,0), rect.value(), 1)
        position = state1.position
        pygame.draw.circle(screen, (255, 0, 0), position.value(), 1)

if __name__ == "__main__":
    options = config.OptionConfig()    
    pygame.init()
    config.Screen()

    background = Background('../res/Background/Bckgrnd4.png')

    warrior_state1 = WarriorState(True, Point(150,195))
    warrior_state2 = WarriorState(False, Point(170,195))

    warrior_ui1 = WarriorUi(warrior_state1, screen, '../res/Char/Rick/Rick.png')
    warrior_ui2 = WarriorUi(warrior_state2, screen, '../res/Char/Ken/Ken.png')
    
    warrior1 = WarriorInputAgent(warrior_state1)
    warrior2 = WarriorInputAgent(warrior_state2)

    game = GameController(screen, background, warrior1, warrior_ui1, warrior2, warrior_ui2)
    game.mainloop()
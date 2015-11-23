from warrior import *
from utils import KEYCONST

DEBUG = True

class WarriorInput():

    def __init__(self):
        self.stick_inputs = [None]
        self.btn_inputs = [None]
        self.inputTick = 0
        self.last_inputs = []

    def reinit(self):
        self.stick_inputs = [None]
        self.btn_inputs = [None]

    def setInputs(self, facingRight, stick_inputs, btn_inputs):
        self.btn_inputs = btn_inputs
        if len(stick_inputs) == 0:
            input_buffer = None
        else:
            input_buffer = stick_inputs
            if facingRight == False:
                for i in range(len(input_buffer)):
                    if input_buffer[i] == KEYCONST.BACK:
                        input_buffer[i] = KEYCONST.FORW
                    elif input_buffer[i] == KEYCONST.FORW:
                        input_buffer[i] = KEYCONST.BACK
                    
        
        if input_buffer != self.stick_inputs[len(self.stick_inputs)-1]:
            self.stick_inputs.append(input_buffer)
            if len(self.stick_inputs) > 12:
                self.stick_inputs.pop(0)
            self.inputTick = 0
        else:
            self.inputTick += 1
            if self.inputTick > 8:
                self.stick_inputs = [input_buffer]
                self.inputTick = 0
        self.print_inputs()

    def input_contains(self, search, index = -1):
        if (len(self.stick_inputs) <= index):
            return False
        if index < 0:
            if (abs(index) > len(self.stick_inputs)):
                return False
            
        if self.stick_inputs[index] == None:
            if search == None:
                return True
            return False
        for input in self.stick_inputs[index]:
            if input == search:
                return True
        return False

    def invert_inputs(self):
        for input in self.stick_inputs :
            if input == None :
                continue
            for i in range(len(input)):
                if input[i] == KEYCONST.BACK:
                    input[i] = KEYCONST.FORW
                elif input[i] == KEYCONST.FORW:
                    input[i] = KEYCONST.BACK

    def print_inputs(self):
        if self.last_inputs == self.stick_inputs and len(self.btn_inputs)==0:
            return
        self.last_inputs = []
        for i in self.stick_inputs:
            self.last_inputs.append(i)
        for input_list in self.stick_inputs:
            print('(', end='')
            if input_list == None :
                print('x) ', end='')
                continue
            for input in input_list:
                if input == KEYCONST.FORW : print('->', end='')
                elif input == KEYCONST.BACK : print('<-', end='')
                elif input == KEYCONST.DOWN : print('|', end='')
                elif input == KEYCONST.UP : print('^', end='')
            print(') ', end='')
        print('(', end='')
        for buttons in self.btn_inputs:
            if buttons == KEYCONST.BTNA : print('A', end='')
            elif buttons == KEYCONST.BTNB : print('B', end='')
            elif buttons == KEYCONST.BTNC : print('C', end='')
        print(') ', end='')
        print()


class WarriorInputAgent:

    def __init__(self, state):
        self.state = state
        self.input = WarriorInput()

    def set_inputs(self, stick_inputs, btn_inputs):
        self.input.setInputs(self.state.facing_right, stick_inputs, btn_inputs)

    def next_action(self, enemy_state):
        if self.input.btn_inputs.count(KEYCONST.BTNA) > 0:
            return LightAttackAction()
        if self.input.btn_inputs.count(KEYCONST.BTNB) > 0:
            return HardAttackAction()
        if self.input.btn_inputs.count(KEYCONST.BTNC) > 0:
            return BlockAction()
        
        if self.input.input_contains(KEYCONST.FORW):
            if self.input.input_contains(KEYCONST.UP, -1):
                return JumpAction(7)
            else:
                return WalkForwAction()
        if self.input.input_contains(KEYCONST.BACK):
            if self.input.input_contains(KEYCONST.UP, -1):
                return JumpAction(-7)
            else:
                return WalkBackAction()
        if self.input.input_contains(KEYCONST.UP, -1):
            return JumpAction()

        return IdleAction()
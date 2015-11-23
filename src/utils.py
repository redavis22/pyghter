import pygame
import os
from math import hypot
from pygame.locals import *

class KEYCONST:
    FORW = 0
    BACK = 1
    DOWN = 4
    UP = 5    
    BTNA = 6
    BTNB = 7
    BTNC = 8

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def value(self):
        return (self.x, self.y)
    
    def __eq__(self,other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False
        
    def __add__(self, other):
        assert(isinstance(other, Point) or isinstance(other, Vector) or isinstance(other, tuple))
        if isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        else:
            return Point(self.x + other.x, self.y + other.y)
            
    def __sub__(self, other):
        assert(isinstance(other, Point) or isinstance(other, Vector) or isinstance(other, tuple))
        if isinstance(other, tuple):
            return Point(self.x - other[0], self.y - other[1])
        else:
            return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        assert(isinstance(other, int))
        return Point(self.x*other, self.y*other)
    
    def __floordiv__(self, other):
        return self.__truediv__(other)
            
    def __truediv__(self, other):
        assert(isinstance(other, int))
        return Point(self.x//other, self.y//other)
            
    def __str__(self):
        return "Point({0}, {1})".format(self.x, self.y)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length()
        
    def length(self):
        '''Sets and returns the vector's length as an integer,
        using the hypot methode of math.py'''
        self.length=hypot(self.x, self.y)
        self.length = int(self.length)
        return self.length
    
    def __eq__(self,other):
        if isinstance(other, Vector):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False
    
    def __add__(self, other):
        assert(isinstance(other, Point) or isinstance(other, Vector) or isinstance(other, tuple))
        if isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            return Vector(self.x + other.x, self.y + other.y)
            
    def __sub__(self, other):
        assert(isinstance(other, Point) or isinstance(other, Vector) or isinstance(other, tuple))
        if isinstance(other, tuple):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            return Vector(self.x - other.x, self.y - other.y)
        
    def __mul__(self, other):
        assert(isinstance(other, Vector) or isinstance(other, int))
        if isinstance(other, int):
            return Vector(other*self.x,other*self.y) ## retourne le vecteur multiple par un scalaire
        else:
            return  self.x*other.x+self.y*other.y ## retourne le produit scalaire
    
    def __floordiv__(self, other):
        assert(isinstance(other, int))
        return Vector(self.x/other, self.y/other) ## retourne le vecteur ayant subi une division scalaire
    
    def __truediv__(self, other):
        return self.__floordiv__(other)
        
    def __str__(self):
        return "Vector({0}, {1})".format(self.x, self.y)


class Rect:
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        if (isinstance(position, Point)):
            self.position = position
        else:
            assert(isinstance(position, tuple))
            assert(len(tuple) > 1)
            assert(isinstance(position[0],int) and isinstance(position[1],int))
            self.position = Point(position[0],position[1])
        self.area = self.width * self.height
    
    def value(self):
        return (self.position.x, self.position.y, self.width, self.height)
    
    def getCenter(self):
        return self.position + (self.width//2, self.height//2)
    
    def collide(self, rect2):
        rect1 = self
        return ((rect1.position.x < rect2.position.x + rect2.width) \
        and (rect1.position.x + rect1.width > rect2.position.x)) \
        and (( rect1.position.y < rect2.position.y + rect2.height) \
        and (rect1.position.y + rect1.height > rect2.position.y))


    def __eq__(self,other):
        if isinstance(other, Rect):
            return (self.width == other.width) and (self.height == other.height)
        else:
            return False
    
    def __str__(self):
        return "Rect({0}, {1}) at {2}x{3}".format(self.width, self.height, self.position.x, self.position.y)



class SpriteSheetLoader:
    def __init__(self,file,sprite_width,sprite_height, fullsheet=False):
        self.sheet = pygame.image.load(os.path.join(file))
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprite_list=self.makeSpritelist()
        if not fullsheet:
            self.removeBlanks(file)
        
    def getSpriteList(self):
        return self.sprite_list
    
    def getSpriteLines(self,*args):
        for arg in args:
            assert(isinstance(arg, int)) # assert it's an array index
            yield self.sprite_list[arg] # return the animation and get to the next one asked
    
    def makeSprite(self,line=0,column=0):
        sprite = pygame.Surface((self.sprite_width, self.sprite_height)).convert_alpha()
        sprite.fill((0,0,0,0))
        sprite.blit(self.sheet, (-(column*self.sprite_width),-(line*self.sprite_height)))
        return sprite
    
    def makeSpritelist(self):
        size = self.sheet.get_size()
        sprite_list=[]
        for i in range(int(size[1]/self.sprite_height)):    
            sprite_line=[]
            for j in range(int(size[0]/self.sprite_width)):
                sprite_line.append(self.makeSprite(i,j))
            sprite_list.append(sprite_line)
        return sprite_list
    
    def testBlankSprite(self,sprite):
        for i in range(self.sprite_width):
            for j in range(self.sprite_height):
                if sprite.get_at((i,j))!=(0,0,0,0):
                    return False
        return True
    
    def removeBlanks(self, file):
        try:
            with open(file.replace('.png', '.txt'), encoding='utf-8') as txtfile:
                i=0
                for line in txtfile:
                    length = int(line)
                    while length < len(self.sprite_list[i]):
                        self.sprite_list[i].pop()
                    i+=1
        except:
            print('creating...')    
            for sprite_line in self.sprite_list:
                j=0
                while j < len(sprite_line):
                    if self.testBlankSprite(sprite_line[j]):
                        sprite_line[j] = None
                    j+=1
            self.write(file)
            
    def write(self,file):
        txtfile = open(file.replace('.png', '.txt'), mode='w', encoding='utf-8')
        for sprite_line in self.sprite_list:
            i=0
            for sprite in sprite_line:
                if sprite == None:
                    break
                else: i+=1
            txtfile.write(str(i))
            txtfile.write('\n')

class InputReader:
    def __init__(self, keysP1, keysP2):
        self.keysP1 = keysP1
        self.keysP2 = keysP2   
        
    def getInputs(self):
        btn_inputs_p1 = []
        stick_inputs_p1 = []
        btn_inputs_p2 = []
        stick_inputs_p2 = []
        special = 0
        
        for event in pygame.event.get():
            
            ## Exit conditions
            if event.type == QUIT:
                print('quit !')
                exit()
            if event.type == KEYDOWN:
                if event.key == K_F5:
                    print('quit !')
                    special = 'QUIT'
                if event.key == K_ESCAPE:
                    print('pause')
                    special = 'PAUSE'
                if event.key == K_F1:
                    special = 1
                if event.key == K_F4:
                    special = 2
                if event.key == K_F3:
                    special = 3
                    
                ## Get Player 1 hit keys
                # print(self.keysP1)
                # print(self.keysP2)
                if event.key == self.keysP1[4]:
                    btn_inputs_p1.append(KEYCONST.BTNA)
                if event.key == self.keysP1[5]:
                    btn_inputs_p1.append(KEYCONST.BTNB)
                if event.key == self.keysP1[6]:
                    btn_inputs_p1.append(KEYCONST.BTNC)
                ## Get Player 2 hit keys
                if event.key == self.keysP2[4]:
                    btn_inputs_p2.append(KEYCONST.BTNA)
                if event.key == self.keysP2[5]:
                    btn_inputs_p2.append(KEYCONST.BTNB)
                if event.key == self.keysP2[6]:
                    btn_inputs_p2.append(KEYCONST.BTNC)
                
                    
        keys=pygame.key.get_pressed()
        ## Get Player 1 move keys
        if keys[self.keysP1[0]]:
            stick_inputs_p1.append(KEYCONST.UP)
        if keys[self.keysP1[1]]:
            stick_inputs_p1.append(KEYCONST.DOWN)
        if keys[self.keysP1[2]]:
            stick_inputs_p1.append(KEYCONST.BACK)
        if keys[self.keysP1[3]]:
            stick_inputs_p1.append(KEYCONST.FORW)   
        ## Get Player 2 key 
        if keys[self.keysP2[0]]:
            stick_inputs_p2.append(KEYCONST.UP)
        if keys[self.keysP2[1]]:
            stick_inputs_p2.append(KEYCONST.DOWN)
        if keys[self.keysP2[2]]:
            stick_inputs_p2.append(KEYCONST.BACK)
        if keys[self.keysP2[3]]:
            stick_inputs_p2.append(KEYCONST.FORW)  
        
        # if stick_inputs_p2:
        #     print(stick_inputs_p2)
        return stick_inputs_p1, btn_inputs_p1, stick_inputs_p2, btn_inputs_p2, special

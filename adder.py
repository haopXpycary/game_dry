from Const import *
from random import randint

class adder:
    def __init__(self,kind,perch,x,y,color=CHColor,eatAble=True,crossAble=True):
        self.kind = kind
        self.perch = perch
        if x<0:
            self.x = randint(1,MaxScrX-1)
        else:
            self.x = x
        if y<0:
            self.y = randint(1,MaxScrY-1)
        else:
            self.y = y
        self.color = color
        self.eatAble = eatAble
        self.crossAble = crossAble
        self.health = 1
        self.bgcolor = White

class wallAdder(adder):
    def __init__(self,x,y,perch,color,health):
        super().__init__(WallAdder,perch,x,y,color,eatAble=False,crossAble=False)
        self.health = health
        self.isbroken = False
        
    def beHit(self,ht=1):
        self.health -= 1
        if self.health <= 0: self.isbroken = True

class bodyAdder(adder):
    def __init__(self,x=-1,y=-1,have=[]):
        super().__init__(BodyAdder,"%",x,y,Black,eatAble=False,crossAble=True)
        self.have = have
        
    def add(self,*havelist):
        for i in havelist: self.have.append(i)
        
class transportAdder(adder):
    def __init__(self,x,y):
        super(TransportAdder,"o",x,y,Black,eatAble=False)
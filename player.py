from copy import deepcopy

from Const import *
from funcTool import *
	
cp = deepcopy

class player:
    def __init__(self,x,y,color=Black):
        self.x = x
        self.y = y
        self.headfor   = Right
        self.lastxy = (x,y)
        self.color = color
        self.state = WAITING
        
        self.handin = None
        self.bag = dict()
        
        self.health    = 20
        self.maxHealth = 20
        self.protect   = 1
        self.isAlive   = True
        self.hitHealth = 4
        
        self.exp       = 0
        self.level     = 1
        self.money     = 0
        
        self.magic     = 10
        self.maxMagic  = 10
        
        self.perch = ">"
        self.way = 0
        
    def give(self,thing):
        if thing in self.bag:
            self.bag[thing] += 1
        else:
            self.bag[thing] = 1
    
    def decthing(self,thing):
        if thing in self.bag:
            if self.bag[thing] > 0: 
                self.bag[thing] -= 1
                return True;
            else: return False
        else: return False
    
    def move(self,x,y):
        self.x   = x
        self.y   = y

    def walk(self,headfor):
        if headfor == self.headfor:
            if headfor == Right:
                if self.x < MaxScrX-1:
                    self.x += 1
            
            if headfor == Left:
                if self.x > 0:
                    self.x -= 1
         
            if headfor == Down:
                if self.y < MaxScrY-1:
                    self.y += 1
         
            if headfor == Up:
                if self.y > 0:
                    self.y -= 1
        
        else:
            self.headfor = headfor
        
        if self.headfor == Right:
            self.perch = ">"
        elif self.headfor == Left:
            self.perch = "<"
        elif self.headfor == Up:
            self.perch = "^"
        elif self.headfor == Down:
            self.perch = "v"
        self.way += 1
        
    def healthChange(self,health):
        self.health += health
        
        if self.health <= 0:
            self.health = 0
            self.isAlive = False
        if self.health >= self.maxHealth:
            self.health = self.maxHealth
            
    def addExp(self,exp):
        self.exp += exp
        if self.exp >= LevelUp(self.level):
            self.exp = 0
            self.level += 1
            self.maxHealth = 5+self.maxHealth
            self.protect = 2+self.protect
            self.hitHealth = 3+self.hitHealth
            self.maxMagic = 4+self.maxMagic
    
    def decMp(self,mp):
        if self.magic >= mp:
            self.magic -= mp
            return True
        else:
            return False
    
    def addMp(self,mp=1):
        if self.magic+mp < self.maxMagic:
            self.magic += mp
        else:
            self.magic = self.maxMagic
            
    def tp(self):
        if self.decMp(2):
            for i in range(6):
                self.walk(self.headfor)
    
    def update(self):
        self.addMp()
        
    def beHit(self,hit):
        if hit < self.protect:return;
        self.healthChange(-(hit-self.protect))
            #print(vars(self))
            
if __name__ == "__main__":
    p = player(0,0)
    print(dir(p))

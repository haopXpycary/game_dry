from Const import *

class animal:
    def __init__(self,x,y,perch,color,health,relationship=Neutrality,hitHealth=0,last=[]):
        self.health = health
        self.hitHealth = hitHealth
        self.color = color
        self.perch = perch
        self.x = x
        self.y = y
        self.relationship = relationship
        self.isAlive = True
        self.headfor = Right
        self.last = last
        
    def walk(self,headfor=None):
        if not headfor: return;
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
                
        self.headfor = headfor
        
    def beHit(self,health):
        self.health -= health
        if self.health <= 0:
            self.isAlive = False
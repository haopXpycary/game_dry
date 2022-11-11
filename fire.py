from Const import *

class fire():
    def __init__(self,per):
        self.x = per.x
        self.y = per.y
        self.headfor = per.headfor
        self.hitHealth = per.hitHealth
        self.color = per.color
        self.hitWall = False
        self.stop    = False
        
        self.firech = ">"
        if self.headfor == Right:
            self.firech = ">"
        elif self.headfor == Left:
            self.firech = "<"
        elif self.headfor == Up:
            self.firech = "^"
        elif self.headfor == Down:
            self.firech = "v"
            
    def run(self):
        headfor = self.headfor
            
        if headfor == Right:
            if self.x < MaxScrX:
                self.x += 1
            else:
                self.hitWall = True
        elif headfor == Left:
            if self.x > 0:
                self.x -= 1
            else:
                self.hitWall = True
        elif headfor == Down:
            if self.y < MaxScrY:
                self.y += 1
            else:
                self.hitWall = True
        elif headfor == Up:
            if self.y > 0:
                self.y -= 1
            else:
                self.hitWall = True
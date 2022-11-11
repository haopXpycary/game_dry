import sys
import tty
import termios
from threading import Thread

from Const import *

class keyboardListen(Thread):
    def __init__(self):
        """    
        sb = keyboardListen()
        sb.start()
        ch = ""
        while True:
            if ch != sb.ch:
                print("\033[1A%s" %sb.ch)
                sb.ch = ch
            sleep(0.01)
        """
        super().__init__()
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno(), termios.TCSANOW)
        self._getch = sys.stdin.read
        self.stop = False
        self.ch = ""
        
    def run(self):
        while not self.stop:
            self.ch = self._getch(1)
        
def cprint(x,y,other,color=White,bgcolor=Black):
    if not other: return;
    scon = "\033[%d;%dH" %(y,x)
    
    if color == Black: con = "\033[30m"
    elif color == Red: con = "\033[31m"
    elif color == Green: con = "\033[32m"
    elif color == Orange: con = "\033[33m"
    elif color == Blue: con = "\033[34m"
    elif color == Purple: con = "\033[35m"
    elif color == DarkGreen: con = "\033[36m"
    elif color == White: con = "\033[37m"
    
    
    if bgcolor == Black: bgcon = "\033[40m"
    elif bgcolor == Red: bgcon = "\033[41m"
    elif bgcolor == Green: bgcon = "\033[42m"
    elif bgcolor == Orange: bgcon = "\033[43m"
    elif bgcolor == Blue: bgcon = "\033[44m"
    elif bgcolor == Purple: bgcon = "\033[45m"
    elif bgcolor == DarkGreen: bgcon = "\033[46m"
    elif bgcolor == White: bgcon = "\033[47m"
    
    print(con+bgcon+scon+str(other))

from copy import deepcopy
from random import randint
class scrControl:
    def __init__(self,x,y):
        #[(char,color,bgcolor),..., #line1
        # (char,color,bgcolor),..., #line2
        #  ...]
        self.scr = []
        self.initscr(x,y)
        self.lastscr = deepcopy(self.scr)
        self.allscr = dict()
        
    def initscr(self,x,y):
        self.scrx = x
        self.scry = y
        for i in range(x*y):
            self.scr.append((" ",BGColor,BGColor))
            
    def update(self,x,y,ch=" ",color=CHColor,bgColor=BGColor,other=None):
        if x<self.scrx and y<self.scry:
            self.scr[y*self.scrx+x] = (ch,color,bgColor)
            if ch != " ": self.allscr[(x,y)] = ch
        if other:
            self.allscr[(x,y)] = other
        if ch == " " and (x,y) in self.allscr:
            del self.allscr[(x,y)]
    
    def show(self):
        for i in range(self.scry):
            for j in range(self.scrx):
                #print(i,j)
                cprint(j+2,i+2,self.scr[i*self.scrx+j][0],self.scr[i*self.scrx+j][1],self.scr[i*self.scrx+j][2])
        self.lastscr = deepcopy(self.scr)
                
    def updateShow(self):
        for i in range(self.scry):
            for j in range(self.scrx):
                if self.scr[i*self.scrx+j] != self.lastscr[i*self.scrx+j]:
                    cprint(j+2,i+2,self.scr[i*self.scrx+j][0],self.scr[i*self.scrx+j][1],self.scr[i*self.scrx+j][2])
        self.lastscr = deepcopy(self.scr)
        
    def setRaid(self,x,y,per):
        self.allscr[(x,y)] = per
        
    def getRaid(self,x,y):
        if (x,y) in self.allscr: return self.allscr[(x,y)] 
        else: return None;

    def hasRaid(self,x,y):
        if (x,y) in self.allscr: return True;
        else: return False;
        
    def delRaid(self,x,y):
        if (x,y) in self.allscr: del self.allscr[(x,y)];
        
    def randRaid(self):
        while True:
            randraid = (randint(0,MaxScrX-1),randint(0,MaxScrY-1))
            if not self.hasRaid(*randraid): return randraid;
            
def clear():
    for k in range(2,20):
        cprint(MaxScrX+3,k," "*11,White);
 
from pickle import dump,load,HIGHEST_PROTOCOL
def saveObject(obj,name,path="obj/"):
    with open(path+name+".pkl","wb") as fp:
        dump(obj, fp, HIGHEST_PROTOCOL)
        
def loadObject(name,path="obj/"):
    with open(path+name+".pkl","rb") as fp:
        return load(fp)
        
def clearObject(name,path="obj/"):
    open(path+name+".pkl","w")
    
def saveWorld(obj,name):
    with open("world/"+name+".wrd","wb") as fp:
        dump(obj, fp, HIGHEST_PROTOCOL)
        
def loadWorld(name):
    with open("world/"+name+".wrd","rb") as fp:
        return load(fp)
        
def clearWorld(name):
    open("world/"+name+".wrd","w")
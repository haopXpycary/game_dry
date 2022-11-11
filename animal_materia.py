from animal import *
from Const import *
from thing_materia import *

def setPig(x,y):
    return animal(x,y,"P",Black,20)
    
def setWolf(x,y):
    return animal(x,y,"W",Black,40,Passively,hitHealth=5,last=[meet_thing,meet_thing])
    
def setDog(x,y):
    return animal(x,y,"D",PER_COLOR,40,Positively,hitHealth=5,last=[meet_thing,meet_thing])
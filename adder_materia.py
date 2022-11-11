from adder import *
from Const import *

def setAdder(kind,perch,x=-1,y=-1,color=CHColor,eatAble=True,crossAble=True):
    return adder(kind,perch,x=-1,y=-1,color=color,eatAble=eatAble,crossAble=crossAble)

def setStoneAdder(x=-1,y=-1):
    return wallAdder(x,y,"#",Black,20)

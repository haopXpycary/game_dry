#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
from time import sleep,strftime
from random import randint,seed,choice
from copy import deepcopy
from gc import collect
from tempfile import TemporaryFile

from Const import *
from player import *
from animal import *
from animal_materia import *
from fire import *
from funcTool import *
from adder import *
from adder_materia import *
from thing import *
from thing_materia import *

if STATE_CONNECTION: 
    from before import *
    seed(tan.port)
else:
    class tan: back = None

logfile = open("./log/log.out","w",buffering=1)
logout = lambda *n: print(strftime("[%H:%M]"),*n,file=logfile)
errfile = open("./log/err.out","w",buffering=1)
sys.stderr = errfile
statefile = open("./obj/type.out","w",buffering=1)
shutilfile = open("./log/shutil.out","w",buffering=1)
userstatefile = TemporaryFile("w+t",buffering=1,encoding="utf-8")

toolprint = lambda n,perch: cprint(n*4+4,MaxScrY+4,perch,White)
print("\033[?25l\033[2J\033[0;0H")
getch = keyboardListen()
getch.start()

i = 0
bodyIndexPointer = 0
toolIndexPointer = 0
index = 0
perRaid = (0,0)
thingChosen = None

print("\033[0;0H"+"+"+"-"*MaxScrX+"+"+"-"*10+"+")
for i in range(2,MaxScrY+2):print("\033[%d;0H" %i+"|"+" "*MaxScrX+"|")
print("\033[%d;0H"%(MaxScrY+2)+"+"+"-"*MaxScrX+"+"+"-"*10+"+")
print("\033[%d;0H"%(MaxScrY+3)+" +"+"---+"*(MaxScrX//3-RAST_TOOL_LABOR))
print("\033[%d;0H"%(MaxScrY+4)+" |"+"   |"*(MaxScrX//3-RAST_TOOL_LABOR))
print("\033[%d;0H"%(MaxScrY+5)+" +"+"---+"*(MaxScrX//3-RAST_TOOL_LABOR))
print("\033[%d;0H"%(MaxScrY+6)+"HP:"+"#"*30)

scr = scrControl(MaxScrX,MaxScrY)
scr.show()

per = player(0,0,PER_COLOR)
per2 = player(5,5,Blue)
#[classAdder,...]
adderList = []
stoneList = []
bodyList  = []
#[classFire,...]
fireList = []
#[classAnimal,...]
animalList = []
for j in range(5):
    stoneList.append(setStoneAdder());sleep(TIME)
animalList.append(setPig(3,8));sleep(TIME)
animalList.append(setWolf(6,9));sleep(TIME)
animalList.append(setDog(6,10));sleep(TIME)
animalList.append(setWolf(6,11));sleep(TIME)
bodyList.append(bodyAdder(3,3));sleep(TIME)
bodyList[0].add(meet_thing,water_thing,sand_thing)
per.give(meet_thing)
cprint(bodyIndexPointer*4+3,MaxScrY+4,">",White)
cprint(bodyIndexPointer*4+5,MaxScrY+4,"<",White)

while True:
    i += 1
    if "" != getch.ch:
        if DISPLAY_MODE == DISPLAY_PLAYER:
            if getch.ch in [Up,Right,Left,Down]:
                per.walk(getch.ch)
            elif getch.ch == OPEN:
                bodyIndexPointer = 0
                for j in bodyList:
                    if j.x == per.x and j.y == per.y:
                        index = bodyList.index(j)
                        DISPLAY_MODE = DISPLAY_BODY
                        clear()
                        lp = 2
                        for k in j.have:
                            if k: cprint(MaxScrX+3,lp," "+k.name,White);lp+=1
                        cprint(MaxScrX+3,2,">",White)
                        break;
            elif getch.ch == TOOL:
                clear()
                DISPLAY_MODE = DISPLAY_TOOL
                
            elif getch.ch == TP:
                per.tp()
            elif getch.ch == FIRE:
                fireList.append(fire(per))
                per.state = FIREING
            elif getch.ch == SAVE:
                saveObject(per,"player")
                saveObject(scr,"screen")
                saveObject(adderList,"adder")
                saveObject(stoneList,"stone")
                saveObject(animalList,"animal")
                statefile.write(FILE_STATE_SAVE)
                
            elif getch.ch == SHUTIL:
                print(strftime("[%H:%M:%S]"),file=shutilfile)
                print("-"*100,file=shutilfile)
                print("|{:<20}|{:<10}|{:<}".format("Name","Shutil","Type"),file=shutilfile)
                sum = 0
                for j in dir():
                    print("|{:<20}|{:<10}|{:<}".format(j,eval("sys.getsizeof(%s)" %j),str(eval("type(%s)"%j))),file=shutilfile)
                    sum += eval("sys.getsizeof(%s)" %j)
                print("|{:<20}|{:<10}|{:<}".format("SUM_OF",sum,"-"),file=shutilfile)
                print("-"*100,file=shutilfile)
                    
        elif DISPLAY_MODE == DISPLAY_BODY:
            if getch.ch in (Up,Down):
                cprint(MaxScrX+3,bodyIndexPointer+2," ",White)
                if getch.ch == Up: bodyIndexPointer -= 1
                if getch.ch == Down: bodyIndexPointer += 1
                if bodyIndexPointer < 0: bodyIndexPointer = 0
                if bodyIndexPointer > 11: bodyIndexPointer = 11
                cprint(MaxScrX+3,bodyIndexPointer+2,">",White)
            
            elif getch.ch == OPEN or getch.ch in (Left,Right):
                DISPLAY_MODE = DISPLAY_PLAYER
                clear()
                bodyIndexPointer = 0
                
            elif getch.ch == CHOOSE:
                if len(bodyList[index].have) > bodyIndexPointer:
                    logout("#########################")
                    # bodyList[index].have.remove(bodyList[index].have[bodyIndexPointer])
                    per.give(bodyList[index].have[bodyIndexPointer])
                    logout(per.bag)
                    bodyList[index].have[bodyIndexPointer] = ""
                    logout("bodyList[index].have:",bodyList[index].have)
                    logout("all(bodyList[index].have):",all(bodyList[index].have))
                    if not any(bodyList[index].have): del bodyList[index]
                    cprint(MaxScrX+4,bodyIndexPointer+2," "*10,White)
                
        elif DISPLAY_MODE == DISPLAY_TOOL:
            # logout("#########################")
            cprint(toolIndexPointer*4+3,MaxScrY+4," ",White)
            cprint(toolIndexPointer*4+5,MaxScrY+4," ",White)
            if getch.ch == Left:
                if toolIndexPointer > 0: toolIndexPointer -= 1
            elif getch.ch == Right: 
                if toolIndexPointer < (MaxScrX//3-RAST_TOOL_LABOR-1): toolIndexPointer += 1
            cprint(toolIndexPointer*4+3,MaxScrY+4,">",White)
            cprint(toolIndexPointer*4+5,MaxScrY+4,"<",White)
            
            if getch.ch == CHOOSE:
                getch.ch = TOOL
                per.hand = thingChosen
            
            if getch.ch in (Up,Down,TOOL):
                cprint(toolIndexPointer*4+3,MaxScrY+4,"<",White)
                cprint(toolIndexPointer*4+5,MaxScrY+4,">",White)
                DISPLAY_MODE = DISPLAY_PLAYER
                clear()

        getch.ch = ""         

        for j in adderList:
            if j.x == per.x and j.y == per.y:
                if j.eatAble:
                    if j.kind == HpAdder:
                        per.healthChange(+5)
                    elif j.kind == HpAdder2:
                        per.healthChange(+per.health//5)
                    elif j.kind == MoneyAdder:
                        per.money += 1
                    elif j.kind == ExpAdder:
                        per.addExp(1)
                    per.state = EATING
                    adderList.remove(j)
                if j.kind == TransportAdder:
                    saveWorld(scr)
                    scr = scrControl(MaxScrX,MaxScrY)
                    saveObject(animalList,"animal","world/detail/")
                    saveObject(stoneList,"stone","world/detail/")
                    saveObject(adderList,"adder","world/detail/")
                    saveObject(bodyList,"animal","world/detail/")
                    animalList = []
                    stoneList  = []
                    adderList  = []
                    animalList = []
                
        for j in stoneList:
            if j.x == per.x and j.y == per.y and not j.crossAble:
                per.x,per.y = per.lastxy
    sleep(0.01)
    ##########################################################################
    if i%5 == 0:       #display some message.
        if DISPLAY_MODE == DISPLAY_PLAYER:
            cprint(MaxScrX+3,2,"TIME: {:" "5}".format(i//10),White)
            cprint(MaxScrX+3,3,"HP: {:" "3}/{:" "3}".format(per.health,per.maxHealth),White)
            cprint(MaxScrX+3,4,"MP: {:" "3}/{:" "3}".format(per.magic,per.maxMagic),White)
            cprint(MaxScrX+3,5,"Lv: {:" "7}".format(per.level),White)
            cprint(MaxScrX+3,6,"M$: {:" "7}".format(per.money),White)
            cprint(MaxScrX+3,7,"Att: {:" "6}".format(per.hitHealth),White)
            cprint(MaxScrX+3,8,"Prt: {:" "6}".format(per.protect),White)
            cprint(MaxScrX+3,9,"Rid: {:" "3},{:" "2}".format(per.x,per.y),White)
        elif DISPLAY_MODE == DISPLAY_TOOL:
            if toolIndexPointer < len(per.bag):
                tool = list(per.bag.keys())[toolIndexPointer]
                thingChosen = tool
                num  = list(per.bag.values())[toolIndexPointer]
                logout("tool:",tool)
                logout("toolname:",tool.name)
                cprint(MaxScrX+3,2,"Name: {:" "5}".format(tool.name),White)
                cprint(MaxScrX+3,3,"Num: {:" "5}".format(num),White)
                cprint(MaxScrX+3,4,"Chcc: {:" "5}".format(tool.perch),White)
            else:
                clear();
        k = 0
        for j in per.bag:
            if j: 
                toolprint(k,j.perch)
                cprint(k*4+3,MaxScrY+5,"{:->3}".format(str(per.bag[j])),White)
                k += 1
        lp = round((per.health/per.maxHealth)*30)
        # logout("per.health:",lp)
        print("\033[%d;0H"%(MaxScrY+6)+"HP:"+"#"*lp+"."*(30-lp))
        lp = round((per.magic/per.maxMagic)*30)
        print("\033[%d;0H"%(MaxScrY+7)+"MP:"+"#"*lp+"."*(30-lp))
        #lp = round((per.magic/per.maxMagic)*30)
        #print("\033[%d;0H"%(MaxScrY+8)+"MP:"+"#"*lp+"."*(30-lp))
        per.update()
        
    if i%1 == 0:        #fire run and test hit.
        for j in fireList:
            if j.hitWall == True: del fireList[fireList.index(j)]
            j.run()
        
        for j in fireList:
            if j.x == per.x and j.y == per.y and j.color != per.color:
                per.beHit(j.hitHealth)
                j.hitWall = True
            if j.x == per2.x and j.y == per2.y and j.color != per2.color:
                j.hitWall = True
            for k in stoneList:
                if j.x == k.x and j.y == k.y and not k.crossAble:
                    k.beHit();
                    if k.isbroken: stoneList.remove(k)
                    j.hitWall = True;break
            for k in animalList:
                if j.x == k.x and j.y == k.y and j.color != k.color:
                    k.beHit(j.hitHealth);
                    if not k.isAlive: 
                        animalList.remove(k)
                        if k.last: bodyList.append(bodyAdder(k.x,k.y,k.last))
                    j.hitWall = True;break
                    
    if i%400 == 0:      #append adder
        adderList.append(setAdder(HpAdder,"+",color=Green));sleep(TIME)
        adderList.append(setAdder(MoneyAdder,"$",color=Orange));sleep(TIME)
        adderList.append(setAdder(ExpAdder,"*",color=Blue));sleep(TIME)
        adderList.append(setAdder(HpAdder2,"+",color=Red));sleep(TIME)    
        
    if i%10 == 0 and not STATE_CONNECTION and TEST_RATION: #per2 random move.
        # per2.x,per2.y = scr.randRaid()
        headfor = choice([Right,Left,Up,Down])
        per2.walk(headfor)
        per2.walk(headfor)
        fireList.append(fire(per2))
        
    if i%10 == 0:
        WAR_STATE = False
        for k in animalList:
            k.walk(choice([Right,Left,Up,Down]))
            if k.relationship == Passively:
                WAR_STATE = True
                fireList.append(fire(k))
                
            elif  k.relationship == Positively:
                if WAR_STATE:
                    k.walk(per.headfor)
                    fireList.append(fire(k))
                    
    for j in adderList:
        scr.update(j.x,j.y,j.perch,j.color,j.bgcolor)
    for j in stoneList:
        scr.update(j.x,j.y,j.perch,j.color,j.bgcolor)
    for j in fireList:
        scr.update(j.x,j.y,j.firech,j.color)
    for j in animalList:
        scr.update(j.x,j.y,j.perch,j.color)
    for j in bodyList:
        scr.update(j.x,j.y,j.perch,j.color)
        
    scr.update(per.x,per.y,per.perch,per.color)
    scr.update(per2.x,per2.y,per2.perch,per2.color)
    scr.updateShow()
    
    scr.update(per.x,per.y)
    scr.update(per2.x,per2.y)
    for j in fireList: scr.update(j.x,j.y)
    for j in animalList: scr.update(j.x,j.y)
    #for j in bodyList: scr.update(j.x,j.y)

    state = "%d,%d,%s,%s" %(per.x,per.y,per.perch,per.state)
    per.state = WAITING
    per.lastxy = (per.x,per.y)
    tan.give = state
    back = tan.back
    if back:
        scr.update(per2.x,per2.y)
        back = back.scrlit(",")
        per2.x = int(back[0])
        per2.y = int(back[1])
        per2.perch = back[2]
        per2.state = back[3]
        if per2.state == FIREING: fireList.append(fire(per2))
        elif per2.state == EATING:
            for j in adderList:
                if j.x == per2.x and j.y == per2.y and j.eatAble:
                    del adderList[adderList.index(j)]
                    
    if per.isAlive == False:
        cprint(MaxScrX+3,10,"YOU LOST!",White)
    if per2.isAlive == False:
        cprint(MaxScrX+3,10,"YOU WIN!",White)
    collect() #Free shutil.
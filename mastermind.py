# mastermind.py
# Bao Nguyen
# CSC 110
# November 23,2022

# This program creates a Mastermind game.

from graphics import*
from random import*

def setBoard(win):
    board = Rectangle(Point(3,100), Point(350,500))
    board.setWidth(5)
    board.draw(win)

    sideline = Line(Point(250,100), Point(250,500))
    sideline.setWidth(5)
    sideline.draw(win)

    divline = Line(Point(0,140), Point(350,140))
    divline.setWidth(2)
    divline.draw(win)

    divlineList = objectMultiplier(win,divline,1,9,40,0)
    
    checkbox = Rectangle(Point(250,60),Point(350,100))
    checkbox.setFill("Crimson")
    checkbox.setWidth(2)
    checkbox.draw(win)

    check = Text(Point(300,80), "CHECK")
    check.setFill("Gold")
    check.setSize(19)
    check.setStyle("bold")
    check.draw(win)

    checkboxList = [checkbox]

    againbox = Rectangle(Point(250,500),Point(350,550))
    againbox.setFill("Light Green")
    againbox.setWidth(2)
    againbox.draw(win)

    again = Text(Point(300,525), "Play Again")
    again.setFill("White")
    again.setSize(14)
    again.setStyle("bold")
    again.draw(win)

    againboxList = [againbox]

    exitbox = Rectangle(Point(250,550),Point(350,600))
    exitbox.setFill("Red")
    exitbox.setWidth(2)
    exitbox.draw(win)

    exitt = Text(Point(300,575), "EXIT")
    exitt.setFill("White")
    exitt.setSize(20)
    exitt.setStyle("bold")
    exitt.draw(win)

    exitboxList = [exitbox]

    playcirc = Circle(Point(50,480),15)
    playcirc.setFill("Grey")
    playcirc.setWidth(3)
    playcirc.draw(win)
        
    playcircList = objectMultiplier(win,playcirc,4,10,-40,50)

    hintcirc = Circle(Point(262.5,480),7)
    hintcirc.setFill("Grey")
    hintcirc.setWidth(2)
    hintcirc.draw(win)

    hintcircList = objectMultiplier(win,hintcirc,4,10,-40,25)

    keycirc = Circle(Point(50,525),15)
    keycirc.setWidth(3)
    keycirc.draw(win)
        
    keycircList = objectMultiplier(win,keycirc,4,2,50,50)

    keyColorList = ["Red", "Blue", "Yellow", "Green", "Pink", "White", "Black", "Purple"]

    for i in range (8):
        keycircList[i].setFill(keyColorList[i])

    codecirc = Circle(Point(50,70),15)
    codecirc.setWidth(3)
    codecirc.draw(win)
        
    codecircList = objectMultiplier(win,codecirc,4,1,0,50)

    for i in range (4):
        codecircList[i].setFill("Grey")

    rowColorList = []
    for i in range (40):
        rowColorList.append("Grey")

    return keyColorList,keycircList,playcircList,checkboxList,againboxList,exitboxList,rowColorList,hintcircList,codecircList
    
    
def objectMultiplier(win,objectt,rowLength,columnLength,rowDistance,columnDistance):
    objectList = [objectt]
    tempList = [objectt]
    for i in range (rowLength-1):
        objectt = objectt.clone()
        objectt.move(columnDistance,0)
        objectt.draw(win)
        objectList.append(objectt)
        tempList.append(objectt)

    for i in range (columnLength-1):
        for j in range (rowLength):
            tempList[j] = tempList[j].clone()
            tempList[j].move(0,rowDistance)
            tempList[j].draw(win)
            objectList.append(tempList[j])
    return objectList

def makeCode(keyColorList):
    codeList = []
    codeLockList = []
    rowLockList = []
    for i in range (4):
        code = keyColorList[randint(0,7)]
        codeList.append(code)
    for i in range (10):
        for j in range (4):
            code = codeList[j]
            codeList.append(code)
            codeLockList.append(False)
            rowLockList.append(False)
    return codeList, codeLockList, rowLockList
            
def makeHitBox(objectList):
    left = []
    right = []
    up = []
    down = []

    for i in range (len(objectList)):
        l = (objectList[i].getP1()).getX()
        r = (objectList[i].getP2()).getX()
        u = (objectList[i].getP1()).getY()
        d = (objectList[i].getP2()).getY()
        left.append(l)
        right.append(r)
        up.append(u)
        down.append(d)
    return left, right, up, down

def chooseColor(win,keyColorList,l,r,u,d,click,color,validClick):
    if click != 0:
        p = click
    else:
        p = win.getMouse()

    for i in range (8):
        if p.getX()>l[i] and p.getX()<r[i] and p.getY()>u[i] and p.getY()<d[i]:
            color = keyColorList[i]
            validClick = validClick + 1
            return color,0,validClick
        
    return color,p,validClick

def setColor(win,color,playcircList,rowColorList,l,r,u,d,row,click,validClick):
    if click != 0:
        p = click
    else:
        p = win.getMouse()
        
    for i in range (row*4-4,row*4):
        if p.getX()>l[i] and p.getX()<r[i] and p.getY()>u[i] and p.getY()<d[i] and color != None:
            playcircList[i].setFill(color)
            rowColorList[i] = color
            validClick = validClick + 1
            return rowColorList,0,validClick
        
    return rowColorList,p,validClick
    
def checkRow(win,l,r,u,d,rowColorList,row,click,validClick):
    rowFilled = 0
    for i in range (row*4-4,row*4):
        if rowColorList[i] != "Grey":
            rowFilled = rowFilled + 1
            
    if click != 0:
        p = click
    else:
        p = win.getMouse()
        
    if p.getX()>l[0] and p.getX()<r[0] and p.getY()>u[0] and p.getY()<d[0] and rowFilled==4:
        validClick = validClick + 1
        return True,0,validClick
    
    return False,p,validClick

def checkWin(row,rowColorList,codeList,rowLockList,codeLockList,hintcircList):
    redBall = 0
    whiteBall = 0
    for i in range (row*4-4,row*4):
        if rowColorList[i] == codeList[i]:
            redBall = redBall + 1
            rowLockList[i] = True
            codeLockList[i] = True
            
    for i in range (row*4-4,row*4):
        for j in range (row*4-4,row*4):
            if rowColorList[i] == codeList[j] and rowLockList[i] == False and codeLockList[j] == False:
                whiteBall = whiteBall + 1
                rowLockList[i] = True
                codeLockList[j] = True
                
    for i in range (row*4-4, row*4-4 + redBall):
        hintcircList[i].setFill("Red")
        
    for i in range (row*4-4 + redBall,row*4-4 + redBall + whiteBall):
        hintcircList[i].setFill("White")

    if redBall == 4:
        return True
    else:
        return False

def checkClick(win,l,r,u,d,click,validClick):
    if validClick != 0:
        return False,0,validClick
    if click != 0:
        p = click
    else:
        p = win.getMouse()

    if p.getX()>l[0] and p.getX()<r[0] and p.getY()>u[0] and p.getY()<d[0]:
        validClick = validClick + 1
        return True,0,validClick

    return False,p,validClick

def endGame(win,victory,codecircList,codeList,lagain,ragain,uagain,dagain,lexit,rexit,uexit,dexit):
    winbox = Rectangle(Point(0,0),Point(350,50))
    winbox.setFill("Black")
    winbox.setWidth(2)
    winbox.draw(win)
        
    if victory == True:
        endSign = Text(Point(175,25), "CONGRATULATIONS! YOU WON!")
    else:
        endSign = Text(Point(175,25), "SORRY! YOU LOST!")
            
    endSign.setFill("Orange")
    endSign.setSize(16)
    endSign.setStyle("bold")
    endSign.draw(win)

    for i in range (4):
        codecircList[i].setFill(codeList[i])
            
    playAgain = False
    exitGame = False
    validClick = 0
    while playAgain == False and exitGame == False:
        if validClick == 0:
            click = 0
        validClick = 0
        playAgain, click, validClick = checkClick(win,lagain,ragain,uagain,dagain,click,validClick)
        exitGame, click, validClick = checkClick(win,lexit,rexit,uexit,dexit,click,validClick)

    return playAgain,exitGame

def main():
    playAgain = True
    exitGame = False
    while playAgain == True and exitGame == False:
        win = GraphWin("Mastermind",350,600)
        win.setBackground("Dark Goldenrod")
                
        keyColorList,keycircList,playcircList,checkboxList,againboxList,exitboxList,rowColorList,hintcircList,codecircList = setBoard(win)
        
        codeList,codeLockList,rowLockList = makeCode(keyColorList)

        lkey,rkey,ukey,dkey = makeHitBox(keycircList)
        
        lplay,rplay,uplay,dplay = makeHitBox(playcircList)

        lbox,rbox,ubox,dbox = makeHitBox(checkboxList)
        
        lagain,ragain,uagain,dagain = makeHitBox(againboxList)
        
        lexit,rexit,uexit,dexit = makeHitBox(exitboxList)

        row = 0
        victory = False
        color = None
        validClick = 0
        #print(codeList[:4])
        
        while victory == False and row < 10:
            checked = False
            row = row + 1
            
            while checked == False:
                if validClick == 0:
                    click = 0
                validClick = 0
                
                color,click,validClick = chooseColor(win,keyColorList,lkey,rkey,ukey,dkey,click,color,validClick)
                rowColorList,click,validClick = setColor(win,color,playcircList,rowColorList,lplay,rplay,uplay,dplay,row,click,validClick)
                checked, click,validClick = checkRow(win,lbox,rbox,ubox,dbox,rowColorList,row,click,validClick)

            victory = checkWin(row,rowColorList,codeList,rowLockList,codeLockList,hintcircList)

        playAgain,exitGame = endGame(win,victory,codecircList,codeList,lagain,ragain,uagain,dagain,lexit,rexit,uexit,dexit)

        if playAgain == True:
            win.close()

    win.close()

main()

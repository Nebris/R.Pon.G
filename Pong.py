import pygame,sys,random
widthScreen=800
heightScreen=int(widthScreen*9.0/16.0)
pMenuHeight=heightScreen/5*3
pMenuWidth=widthScreen/4
fps=60

padWidth=heightScreen/50

"""key reference:
w=119
s=115
up=273
down=274
p=112
esc=27
"""

black=(0,0,0)
white=(255,255,255)
grey=[100,100,100]

player = {"pos": [padWidth, (heightScreen / 2) - (padWidth / 2)], "height": 100, "speed": 3, "upkey": 119, "downkey": 115,
        "color": white, "dmg":1,"hp":2}
enemy = {"pos": [widthScreen - (padWidth * 2), (heightScreen / 2) - (padWidth / 2)], "height": 100, "speed": 3,
        "upkey": 273, "downkey": 274, "color": white, "dmg":1,"hp":2}

def drawPaddle(paddle):
    if pause:
        pygame.draw.rect(screen, grey, (paddle["pos"], (padWidth, paddle["height"])))
    else:
        pygame.draw.rect(screen,paddle["color"],(paddle["pos"],(padWidth,paddle["height"])))

def movePaddle(paddle):
    keys=pygame.key.get_pressed()
    if keys[paddle["upkey"]]:
        paddle["pos"][1]-=paddle["speed"]
    if keys[paddle["downkey"]]:
        paddle["pos"][1] += paddle["speed"]
    if paddle["pos"][1]<0:
        paddle["pos"][1]=0
    if paddle["pos"][1]>heightScreen-paddle["height"]:
        paddle["pos"][1]=heightScreen-paddle["height"]

def drawBall(ball):
    if pause:
        pygame.draw.circle(screen, grey, ball["pos"], ball["radius"])
    else:
        pygame.draw.circle(screen,ball["color"],ball["pos"],ball["radius"])

def ballMove(ball,pad1,pad2):
    #if pad2 hits the ball
    if ball["xdir"]==1 and pad2["pos"][1]<ball["pos"][1]<pad2["pos"][1]+pad2["height"] and ball["pos"][0]>pad2["pos"][0]-ball["radius"]:
        ball["xdir"]=-1
        ball["ydir"]+=int(((ball["pos"][1]-float(pad2["pos"][1]))/pad2["height"])*6)-3
        if ball["ydir"]<-4:
            ball["ydir"]=-4
        elif ball["ydir"]>4:
            ball["ydir"]=4
    #if pad1 hits the ball
    elif ball["xdir"]==-1 and pad1["pos"][1]<ball["pos"][1]<pad1["pos"][1]+pad1["height"] and ball["pos"][0]<pad1["pos"][0]+ball["radius"]+padWidth:
        ball["xdir"]=1
        ball["ydir"]+=int(((ball["pos"][1]-float(pad1["pos"][1]))/pad1["height"])*6)-3
        if ball["ydir"]<-4:
            ball["ydir"]=-4
        elif ball["ydir"]>4:
            ball["ydir"]=4
    #if ball hits roof or bottom
    if ball["pos"][1]<=0+ball["radius"] and ball["ydir"]<0:
        ball["ydir"]=-ball["ydir"]
    elif ball["pos"][1]>=heightScreen-ball["radius"] and ball["ydir"]>=0:
        ball["ydir"]=-ball["ydir"]
    #finally moves the ball
    ball["pos"][0] += ball["xdir"] * ball["speed"]
    ball["pos"][1] += ball["ydir"] * ball["speed"]

def hitcalc(ball,pad1,pad2,gamemode):
    #if ball hits the left side
    if ball["pos"][0]<=ball["radius"]:
        pad1["hp"]-=pad2["dmg"]
        ball["pos"]=[widthScreen/2,heightScreen/2]
        ball["xdir"]=1
        ball["ydir"] = random.choice([1, -1])
    #if ball hits the right side
    elif gamemode[0]=="b" and ball["pos"][0]>=widthScreen-ball["radius"]:
        pad2["hp"]-=pad1["dmg"]
        ball["pos"]=[widthScreen/2,heightScreen/2]
        ball["xdir"]=-1
        ball["ydir"]=random.choice([1,-1])
    elif gamemode[0]=="w" and ball["pos"][0]>=widthScreen - (padWidth * 2)+ball["radius"]:
        pad2["hp"] -= pad1["dmg"]
        ball["pos"] = [widthScreen / 2, heightScreen / 2]
        ball["xdir"] = -1
        ball["ydir"] = random.choice([1, -1])
    if pad2["hp"]<=0:
        return False
    elif pad1["hp"]<=0:
        return True

def centerText(text,size,pos,pausable,box=False,clickable=False):
    font=pygame.font.SysFont(None,size)
    if pause and pausable:
        text1=font.render(text,1,grey)
    else:
        text1=font.render(text,1,white)
    newSize=text1.get_size()
    newPos=(pos[0]-newSize[0]/2,pos[1]-newSize[1]/2)
    screen.blit(text1,newPos)
    if box:
        boxSize=(newSize[0]+newSize[1]/3,newSize[1]+newSize[1]/3)
        boxPos=(pos[0]-boxSize[0]/2,pos[1]-boxSize[1]/2)
        if pause and pausable:
            pygame.draw.rect(screen, grey, (boxPos, boxSize), 1)
        else:
            pygame.draw.rect(screen,white,(boxPos,boxSize),1)
        if clickable and pygame.mouse.get_pressed()[0]:
            mPos=pygame.mouse.get_pos()
            if boxPos[0]<mPos[0]<boxPos[0]+boxSize[0] and boxPos[1]<mPos[1]<boxPos[1]+boxSize[1]:
                return True

def convertPad(pad):
    tempPad=pad
    tempPad["maxhp"]=pad["hp"]
    return tempPad

def drawPause(pause,pXPos,options,controls,pad1):
    pygame.draw.rect(screen,black,((widthScreen/2-pMenuWidth/2-pXPos,heightScreen/5),(pMenuWidth,pMenuHeight)))
    pygame.draw.rect(screen, white, ((widthScreen / 2 - pMenuWidth / 2-pXPos, heightScreen / 5), (pMenuWidth, pMenuHeight)),pMenuHeight/100)
    centerText("Pause",heightScreen/8,(widthScreen/2-pXPos,heightScreen/5+pMenuHeight/6),False)
    if pXPos!=0:
        pygame.draw.rect(screen, black,((widthScreen / 2 - pMenuWidth / 2 + pXPos, heightScreen / 5), (pMenuWidth, pMenuHeight)))
        pygame.draw.rect(screen, white,((widthScreen / 2 - pMenuWidth / 2 + pXPos, heightScreen / 5), (pMenuWidth, pMenuHeight)),pMenuHeight / 100)
        if controls:
            centerText("Controls", heightScreen / 8, (widthScreen / 2 + pXPos, heightScreen / 5 + pMenuHeight / 6), False)
            click=pygame.mouse.get_pressed()[0]
            mPos=pygame.mouse.get_pos()
            wsRect=(widthScreen/2+pMenuWidth/8,heightScreen/5+pMenuHeight/12*6-pMenuHeight/20,pMenuWidth/8*6,pMenuHeight/10)
            updownRect=(widthScreen / 2 + pMenuWidth / 8, heightScreen / 5 + pMenuHeight / 12 * 9  - pMenuHeight / 20,pMenuWidth / 8 * 6, pMenuHeight / 10)
            if pad1["upkey"]==119:
                pygame.draw.rect(screen,grey,wsRect)
                pygame.draw.rect(screen, black, updownRect)
            elif pad1["upkey"]==273:
                pygame.draw.rect(screen,black,(widthScreen/2+pMenuWidth/8,heightScreen/5+pMenuHeight/12*6-pMenuHeight/20,pMenuWidth/8*6,pMenuHeight/10))
                pygame.draw.rect(screen, grey, (widthScreen / 2 + pMenuWidth / 8, heightScreen / 5 + pMenuHeight / 12 * 9 - pMenuHeight / 20,pMenuWidth / 8 * 6, pMenuHeight / 10))
            if click and wsRect[0]<mPos[0]<wsRect[0]+wsRect[2] and wsRect[1]<mPos[1]<wsRect[1]+wsRect[3]:
                if pad1["upkey"]==273:
                    pad1["upkey"]=119
                    pad1["downkey"]=115
            elif click and updownRect[0]<mPos[0]<updownRect[0]+updownRect[2] and updownRect[1]<mPos[1]<updownRect[1]+updownRect[3]:
                if pad1["upkey"]==119:
                    pad1["upkey"]=273
                    pad1["downkey"]=274
            centerText("W and S",heightScreen/15,(widthScreen/2+pXPos,heightScreen/5+pMenuHeight/12*6),False)
            centerText("Up and Down",heightScreen/15,(widthScreen/2+pXPos,heightScreen/5+pMenuHeight/12*9),False)
        elif options:
            centerText("Options", heightScreen / 8, (widthScreen / 2 + pXPos, heightScreen / 5 + pMenuHeight / 6),False)
            centerText("there is no options", heightScreen/15,(widthScreen/2+pXPos,heightScreen/2),False)
    if centerText("Back to game",heightScreen/15,(widthScreen/2-pXPos,heightScreen/5+pMenuHeight/12*4),False,True,True):
        pause=False
        controls=False
        options=False
        pXPos=0
    elif centerText("Controls",heightScreen/15,(widthScreen/2-pXPos,heightScreen/5+pMenuHeight/12*6),False,True,True):
        pXPos=pMenuWidth/2
        controls=True
        options=False
    elif centerText("Options",heightScreen/15,(widthScreen/2-pXPos,heightScreen/5+pMenuHeight/12*8),False,True,True):
        pXPos=pMenuWidth/2
        options=True
        controls=False
    elif centerText("Quit battle",heightScreen/15,(widthScreen/2-pXPos,heightScreen/5+pMenuHeight/12*10),False,True,True):
        pXPos=0
        pause = False
        controls = False
        options = False
    return pause,pXPos,controls,options

def botMove(ball,pad2,gamemode):
    if gamemode=="bot1":
        if ball["xdir"]>0:
            if ball["pos"][1]<pad2["pos"][1]+pad2["height"]/4:
                pad2["pos"][1]-=pad2["speed"]
                if pad2["pos"][1]<=0:
                    pad2["pos"][1]=0
            elif ball["pos"][1]>pad2["pos"][1]+pad2["height"]/4*3:
                pad2["pos"][1]+=pad2["speed"]
                if pad2["pos"][1]+pad2["height"]>=heightScreen:
                    pad2["pos"][1]=heightScreen-pad2["height"]

def pong(playerpad,enemypad,gamemode):
    global screen
    global pause

    pygame.init()
    screen=pygame.display.set_mode((widthScreen,heightScreen))
    fpsclock=pygame.time.Clock()

    pause=False
    pXPos=0
    options=False
    controls=False
    status=None

    pad1=convertPad(playerpad)
    pad2=convertPad(enemypad)
    paddles=[pad1,pad2]
    ball={"pos":[widthScreen/2,heightScreen/2],"radius":heightScreen/40,"color":white,"speed":2,"xdir":random.choice([1,-1]),"ydir":random.choice([1,-1])}

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==112:
                    pause=not pause
                    controls=False
                    options=False
                    pXPos=0
                if event.key==27:
                    if pause:
                        pause=False
                        controls=False
                        options=False
                        pXPos=0
        screen.fill(black)

        if not pause:
            movePaddle(pad1)
            movePaddle(pad2)
            botMove(ball,pad2,gamemode)
            ballMove(ball,pad1,pad2)
            status=hitcalc(ball,pad1,pad2,gamemode)
            if status==True:
                return status
            elif status==False:
                return status
        #draw stuff
        for x in xrange(2):
            centerText((str(paddles[x]["hp"])+"/"+str(paddles[x]["maxhp"])),heightScreen/10,(widthScreen/4+widthScreen/4*(2*x),heightScreen/10),True)
            drawPaddle(paddles[x])
        drawBall(ball)
        if pause:
            pause,pXPos,controls,options=drawPause(pause,pXPos,options,controls,pad1)

        pygame.display.update()
        fpsclock.tick(fps)

print pong(player,enemy,"bot1")

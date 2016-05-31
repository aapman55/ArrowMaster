from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from numpy import *
import datetime
import sys

from AapUtils import *
from GameObjects import *

window = 0                                             # glut window number
width, height = 1280, 720                              # window size
horAngle = 0
verAngle = 0
upvelo = 0
upacc = 0
jump = False
player = Player(0,0,0,0.5,1)
gamestate = 1
Menurotangle = 0;
buttonlist = []
menutekstnum = 0
roundnr = 1
power = 0
follow = True
DEBUG = False
MAX_ROUNDS = 10
roundScore = 0
score = 0
highScore = 0


def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x , y+height)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x +width, y)                          # top left point
    glEnd()                                            # done drawing a rectangle

def draw_circle(x,y,radius,segments):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2d(x,y)
    for i in range(0,segments+1):
        glVertex2f(x+radius*cos(2*pi/segments*i),y+radius*sin(2*pi/segments*i))
    glEnd()

def drawLine(x1,y1,z1,x2,y2,z2):
    glBegin(GL_LINES)
    glVertex3f(x1,y1,z1)
    glVertex3f(x2,y2,z2)
    glEnd()

def toRadian(deg):
	return (deg*pi/180)            

def refresh2d(width, height):
    glViewport(0, 0, width, height)    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(width)/height,  0.001,  100);
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
def drawMenu():
    global Menurotangle
    menutitlesize = 50
    buttondown = 0
    Menurotangle +=0.1
    glRotatef(Menurotangle,0,1,0)    
    skybox.draw()    
    font.drawString('Arrow Master',menutitlesize,(glutGet(GLUT_WINDOW_WIDTH)-font.getWidth(menutitlesize,'Arrow Master'))/2.0,50,0,0,0)
    changeto2D()
    glColor3f(0,0,0)
    draw_rect(0,650,1280,b1.height)
    backto3D()
    for a in range(len(buttonlist)):
        if(buttondown == 0):
            buttondown = buttonlist[a].isButton()
        else:
            buttonlist[a].isButton()
        buttonlist[a].draw()
        
    # update mouselocation for the buttons
    Button.mouselocX = Mouse.x
    Button.mouselocY = Mouse.y
    global menutekstnum
    if(buttondown > 0 and Mouse.leftdown):
        if(buttondown == 1):
            global gamestate, horAngle, verAngle,board1\
                   , roundnr, power, arrow, score
            gamestate = 2
            Mouse.setGrabbed(True)            
            horAngle = 0
            verAngle = 0
            board1 = Board.generateBoard()
            roundnr = 1
            Mouse.dx=0
            Mouse.dy = 0
            power = 0
            arrow = Arrow(3,1,0,0,cube)
            score = 0
            menutekstnum = 0
            glutPostRedisplay()
        if(buttondown==2):
            menutekstnum = 2
        if(buttondown==3):
            menutekstnum=3
        if(buttondown==4):
            menutekstnum = 4
        if(buttondown==5):
            with open('highscore.high','w') as f:
                f.write(str(highScore))
            sys.exit()
    elif(Mouse.leftdown):        
        menutekstnum = 0
    # Draw tekst
    if(menutekstnum==2):
        font.drawString('Shoot your arrow at the board, do this by holding ',20,50,200,0,0,0)
        font.drawString('the space bar. Hold the space bar longer to give ',20,50,250,0,0,0)
        font.drawString('more power. Use the mouse to rotate the arrow.',20,50,300,0,0,0)
        font.drawString('F12 - Toggle arrow following mode',20,50,400,0,0,0)
        font.drawString('ESC - Terminate game and return to menu',20,50,450,0,0,0)
    if(menutekstnum == 3):
        w = font.getWidth(30,'Highscore: '+str(highScore))
        h = font.getHeight(30)
        font.drawString('Highscore: '+str(highScore),30,(1280-w)/2.0,(720-h)/2.0,0,0,0)
    if(menutekstnum == 4):
        font.drawString('Mohammed Haddaoui/4205596: Algorithm',30,50,250,0,0,0)
        font.drawString('Zhi-Li Liu/4146557: Graphics',30,50,350,0,0,0)
    refresh2d(width,height)
    glutSwapBuffers()

def drawGame():                                            # ondraw is called all the time
    global currentTime, gamestate, roundnr   
    
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()

    # reset position
    glPushMatrix()
    
    glRotatef(-verAngle,1,0,0)
    glRotatef(horAngle,0,1,0)
    skybox.draw()
    if(follow):        
        glTranslatef((arrow.dist-4)*sin(radians(arrow.horAngle)),-arrow.height+0.5,(arrow.dist-4)*cos(radians(arrow.horAngle)))

    glTranslatef(-player.locX,-(player.locY+player.height),-player.locZ)
    
    #update light positions
    glPushMatrix()
    glLight( GL_LIGHT0, GL_POSITION, [25,25,-25]);
    glEnable(GL_TEXTURE_2D)
    sand.bind()
    glMaterialfv(GL_FRONT, GL_AMBIENT,[0.8,0.8,0.8,1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,[0.5,0.5,0.5,1.0])
    glBegin(GL_QUADS)    
    glTexCoord2f(0,0);glVertex3f(-25,0, -25);
    glTexCoord2f(0,25);glVertex3f(-25,0, 25);
    glTexCoord2f(25,25);glVertex3f(25,0, 25);
    glTexCoord2f(25,0);glVertex3f(25,0, -25);
    glEnd()
    if(DEBUG):
        draworigin()

    board1.draw()
    glPopMatrix()
    arrow.draw()
    glPopMatrix()
    font.drawString('Round: '+str(min(roundnr,10))+'/'+str(MAX_ROUNDS),30,0,0)
    font.drawString('Score: '+str(score),30,0,50,0,1,0)
    powerbar.draw(power)
    refresh2d(width,height)               

    Mouse.warp()
    
    previousTime = currentTime
    currentTime = glutGet(GLUT_ELAPSED_TIME)
    deltaTime = currentTime-previousTime
    if(roundnr<MAX_ROUNDS+1):
        global roundScore
        arrow.update(deltaTime, board1,horAngle,verAngle)
        if(arrow.hitboard):
            if(arrow.tomidpoint<0.95):
                roundScore = 1
            if(arrow.tomidpoint<0.78):
                roundScore = 2
            if(arrow.tomidpoint<0.55):
                roundScore = 3
            if(arrow.tomidpoint<0.3):
                roundScore = 5
            if(arrow.tomidpoint<0.13):
                roundScore = 10
            font.drawString('+'+str(roundScore),30,580,500,0,0,0)
            font.drawString('Press SPACE to continue ...',15,480,580,0,0,0)
        if(arrow.grounded):
            font.drawString('Missed!',30,550,500,0,0,0)
            font.drawString('Press SPACE to continue ...',15,480,580,0,0,0)
            roundScore = 0
        updateGame();
    else:
        global highScore        
            
        stringtodraw = ''
        if(score > highScore):        
            
            stringtodraw = 'Highscore: '+str(score)
        else:
            stringtodraw = 'Score: '+str(score)
        w = font.getWidth(30,stringtodraw)
        font.drawString(stringtodraw,30,(1280-w)/2.0,500,0,0,0)
        w = font.getWidth(15,'Press SPACE to continue ...')
        font.drawString('Press SPACE to continue ...',15,(1280-w)/2.0,580,0,0,0)
        w = font.getWidth(50,'GAME OVER')
        h = font.getHeight(50)
        font.drawString('GAME OVER',50,(1280-w)/2.0,(720-h)/2.0,0,0,0)
        if(Keyboard.keypressed[Keyboard.KEY_SPACE]):            
            gamestate =1
            if(score>highScore):
                highScore = score
            Mouse.setGrabbed(False)
    
    glutSwapBuffers()                                  # important for double buffering
def updateGame():
    global player, upacc, upvelo, jump, currentTime, gamestate, \
           roundnr, board1, power, horAngle, verAngle, arrow
    verAngle += 0.1*Mouse.dy
    horAngle += 0.1*Mouse.dx
    if(verAngle>60):verAngle=60;
    if(verAngle<0):verAngle=0;

    if(Keyboard.keypressed[Keyboard.KEY_SPACE] and (arrow.grounded or arrow.hitboard)):  
        newRound()
        Keyboard.keypressed[Keyboard.KEY_SPACE] = False
        print roundnr
    if(Keyboard.keypressed[Keyboard.KEY_ESC]):        
        gamestate=1
        Mouse.setGrabbed(False)
    if(Keyboard.keypressed[Keyboard.KEY_SPACE] and not arrow.launched):
        power+=0.01
        if(power>1):
            power=1;
    elif((power>0 and not Keyboard.keypressed[Keyboard.KEY_SPACE] and not arrow.launched)):
        arrow.launch(power)
    if(power == 1 and not arrow.launched):
        arrow.launch(power)

        
##
##     #Movement and jumping not required for this game
##        
##    if(not keynotpressed[ord('s')]):       
##        player.locX -= 0.1*sin(radians(horAngle))
##        player.locZ += 0.1*cos(radians(horAngle))
##        
##    if(not keynotpressed[ord('d')]):       
##        player.locX += 0.1*cos(radians(horAngle))
##        player.locZ += 0.1*sin(radians(horAngle))
##        
##    if(not keynotpressed[ord('w')]):       
##        player.locX += 0.1*sin(radians(horAngle))
##        player.locZ -= 0.1*cos(radians(horAngle))
##        
##    if(not keynotpressed[ord('a')]):       
##        player.locX -= 0.1*cos(radians(horAngle))
##        player.locZ -= 0.1*sin(radians(horAngle))
##
##    if(not keynotpressed[32] and not jump):       
##        upacc = 4
##        upvelo = 0
##        jump = True
##        upvelo += 0.05*upacc
##        player.locY = max(0,player.locY+0.05*upvelo)
##    if(player.locY == 0):
##        jump = False
##    else:
##        upvelo += 0.1*upacc
##        player.locY = max(0,player.locY+0.1*upvelo)
##        upacc -=  0.5
def newRound():
    global roundnr, arrow, board1, power, score
    roundnr+=1
    board1 = Board.generateBoard()
    arrow = Arrow(3,1,0,0,cube)
    power = 0
    score+= roundScore
def draworigin():
    glDisable(GL_LIGHTING)
    glLineWidth(6)
    glColor3f(0,0,1)
    drawLine(0,0,0,25,0,0)
    glColor3f(1,0,0)
    drawLine(0,0,0,0,25,0)
    glColor3f(0,1,0)
    drawLine(0,0,0,0,0,25)
    glColor3f(1,1,1)
    glEnable(GL_LIGHTING)
  
  
def specialkeys(key, x, y):

    if(key== GLUT_KEY_F3):
        global DEBUG
        DEBUG = not DEBUG
    if(key== GLUT_KEY_F12):
        global follow
        follow = not follow

def draw():
    if gamestate ==1:
        drawMenu()
    elif gamestate == 2:
        drawGame()

def initGL():

    # Enable back-face culling.
    glCullFace(GL_BACK);
    glEnable(GL_CULL_FACE);
                    
    #Enable Z-buffering
    glEnable(GL_DEPTH_TEST);
                    
    #Enable normalize of normals
    glEnable(GL_NORMALIZE);
    # set depth test
    glClearDepth(1.0);			
    glDepthFunc(GL_LEQUAL);
    # lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight( GL_LIGHT0, GL_AMBIENT, [1,1,1,1]);
    glLight( GL_LIGHT0, GL_DIFFUSE, [1,1,1,1]);
    
# initialization
glutInit()                                             # initialize glut

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      # set window size
glutInitWindowPosition(0, 0)                           # set window position
window = glutCreateWindow("Arrow Master v1.0")                # create window with title
glutDisplayFunc(draw)                                  # set draw function callback
glutIdleFunc(draw)                                     # draw all the time
glutKeyboardFunc(Keyboard.keydown);
glutKeyboardUpFunc(Keyboard.keyup);
glutSpecialFunc(specialkeys);
glutPassiveMotionFunc(Mouse.mousemove);
glutMouseFunc(Mouse.mousefunc)
glutWarpPointer(glutGet(GLUT_WINDOW_WIDTH)/2, glutGet(GLUT_WINDOW_HEIGHT)/2)
currentTime = glutGet(GLUT_ELAPSED_TIME)
initGL()
# read highscore file
try:    
    f = open('highscore.high','r') 
    highScore = int(f.readline().rstrip('\n'))
    f.close()
except:
    print 'file not found, will be created upon exit'
# load texture
sand = Texture.loadFromFile('./resources/textures/sand.jpg')
up = Texture.loadFromFile('./resources/skybox/sky/up.png')
down = Texture.loadFromFile('./resources/skybox/sky/down.png')
north = Texture.loadFromFile('./resources/skybox/sky/north.png')
south = Texture.loadFromFile('./resources/skybox/sky/south.png')
east = Texture.loadFromFile('./resources/skybox/sky/east.png')
west = Texture.loadFromFile('./resources/skybox/sky/west.png')
# setup skybox
skybox = Skybox(up,down,west,east,north,south)
# load models
cube = Model.loadModel('./resources/models','arrow.obj')
cube.generateDL()
# load fonts
font = Font('./resources/fonts/times.png',16,44,0.3)
# set up buttons
Button.setFont(font)
cursloc = 0
b1 = Button(cursloc,650,'   Start   ',1,font,20);cursloc+=b1.width
b2 = Button(cursloc,650, '   Help   ',2,font,20);cursloc+=b2.width
b3 = Button(cursloc,650, '   Highscores   ',3,font,20);cursloc+=b3.width
b4 = Button(cursloc,650, '   Credits   ',4,font,20);cursloc+=b4.width
b5 = Button(cursloc,650,'  Exit  ',5,font,20)
buttonlist.append(b1)
buttonlist.append(b2)
buttonlist.append(b3)
buttonlist.append(b4)
buttonlist.append(b5)
# Generate test board
board1 = Board.generateBoard()
# Make arrow
arrow = Arrow(3,1,0,0,cube)
# Make power bar
powerbar = Statusbar(500,650,300,30,3)
# start everything
glutMainLoop()                                         
